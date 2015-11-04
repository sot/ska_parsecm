import re
import numpy as np
import Chandra.Time

def _coerce_type(val):
    """Coerce the supplied ``val`` (typically a string) into an int or float if
    possible, otherwise as a string.
    """
    try:
        val = int(val)
    except ValueError:
        try:
            val = float(val)
        except ValueError:
            val = str(val)
    return val

def parse_params(paramstr):
    """
    Parse parameters key1=val1,key2=val2,... from ``paramstr``

    Parameter values are cast to the first type (int, float, or str) that
    succeeds.

    :param paramstr: Comma separated string of key=val pairs
    :rtype: dict of key=val pairs
    """
    params = {}
    for opt in paramstr.split(','):
        try:
            key, val = opt.split('=')
            val = val.strip()
            params[key.strip()] = _coerce_type(val)
        except:
            pass  # backstop has some quirks like blank or '??????' fields

    return params

def read_backstop(filename):
    """
    Read commands from backstop file.

    Create dict with keys as follows for each command.  ``paramstr`` is the
    actual string with comma-separated parameters and ``params`` is the
    corresponding dict of key=val pairs.

    ========= ======
    date      char
    time      float
    cmd       char
    params    dict
    paramstr  char
    tlmsid    char
    msid      char
    vcdu      int 
    step      int 
    scs       int 
    ========= ======

    :param filename: Backstop file name
    :returns: list of dict for each command
    """
    bs = []
    for bs_line in open(filename):
        date, vcdu, cmd, paramstr = [x.strip() for x in bs_line.split('|')]
        params = parse_params(paramstr)
        bs.append({'date': date,
                   'time' : Chandra.Time.DateTime(date).secs,
                   'cmd' : cmd,
                   'params' : params,
                   'paramstr' : paramstr,
                   'tlmsid': params.get('TLMSID'),
                   'msid': params.get('MSID'),
                   'vcdu': int(vcdu.split()[0]), # ignore 2nd part of vcdu field
                   'step': params.get('STEP'),
                   'scs': params.get('SCS'),
                   })
    return bs

def read_mm(filename):
    """
    Read maneuver summary file.

    :param filename: Maneuver summary file name
    :rtype: list of dict for each maneuver
    """

    # Parse blocks that look like this:
    #   INITIAL ID:  GG27700
    #                     INITIAL ATTITUDE
    #      START TIME (GMT):  2008:046:05:15:43.038
    #             RA (deg):    160.00000000
    #            DEC (deg):     37.00000000
    #           ROLL (deg):    152.30346378
    #        Dev. from
    #      Opt. Roll (deg):      0.59125433
    #      Sun Angle (deg):    153.65546454
    #    Quaternion:     -0.234681605818   -0.893582206471   -0.277032106484    0.263985977177
    #
    #   FINAL ID:    T_X7800
    #                       FINAL ATTITUDE
    #      STOP TIME (GMT):   2008:046:06:05:20.797
    #             RA (deg):    140.80000000
    #            DEC (deg):    -12.20000000
    #           ROLL (deg):    343.75391110
    #        Dev. from
    #      Opt. Roll (deg):      0.00715175
    #      Sun Angle (deg):    153.86358479
    #    Quaternion:     -0.146233211265   -0.097069667972    0.932362059387    0.316060623455

    mm_text = open(filename).read()
    mm_blocks = mm_text.split("MANEUVER DATA SUMMARY\n")
    manvr_blocks = [x for x in mm_blocks if "INITIAL" in x or "FINAL" in x]
    
    int_obsid = 'IN_IA'

    att_re_dict = { 'obsid': re.compile("ID:\s+(\S+)\S\S"),
                    'time': re.compile("TIME\s*\(GMT\):\s+(\S+)"),
                    'ra': re.compile("RA\s*\(deg\):\s+(\S+)"),
                    'dec': re.compile("DEC\s*\(deg\):\s+(\S+)"),
                    'roll': re.compile("ROLL\s*\(deg\):\s+(\S+)"),
                    'sun_angle': re.compile("Sun Angle\s*\S+\s+(\S+)"),
                    'quat_string': re.compile("Quaternion:\s*((\S+)\s+(\S+)\s+(\S+)\s+(\S+))"),
                    }

    output_re_dict = { 'duration': re.compile("Duration\s*\(sec\):\s+(\S+)"),
                       'angle':  re.compile("Maneuver Angle\s*\(deg\):\s+(\S+)"),
                       }

    manvr_list = []

    for entry in manvr_blocks:
        manvr = {}

        para = entry.split( "\n\n" )
        att_check = re.compile("ATTITUDE")
        att_chunks = filter( att_check.search, para)
        if (len(att_chunks) > 2):
            raise ValueError("Maneuver Summary has too many attitudes in section")
        outdata_check = re.compile("OUTPUT DATA")
        outdata_match = filter( outdata_check.search, para)
        output_data = outdata_match[0]
        
        att_text = { 'initial': att_chunks[0],
                     'final': att_chunks[1] }

        for att in att_text.keys():
            manvr[att] = {}
            for keytype in att_re_dict.keys():
                if att_re_dict[keytype].search(att_text[att]) is None:
                    if (keytype == 'obsid'):
                        # use intermediate attitude label for missing
                        manvr[att][keytype] = int_obsid
                    else:
                        raise ValueError("Maneuver has no obsid")
                else:
                    match = att_re_dict[keytype].search(att_text[att])
                    manvr[att][keytype] = _coerce_type(match.group(1))
                if (keytype == 'quat_string'):
                    manvr[att]['quat'] = [float(s) for s in match.groups()[1:]]

        for keytype in output_re_dict.keys():
            manvr[keytype] = _coerce_type(output_re_dict[keytype].search(output_data).group(1))

        manvr['tstart'] = Chandra.Time.DateTime(manvr['initial']['time']).secs
        manvr['tstop'] = Chandra.Time.DateTime(manvr['final']['time']).secs

        # "correct" manvr start times to line up with AOMANUVR in backstop
        manvr['tstart'] += 10
        manvr['initial']['time'] = Chandra.Time.DateTime(manvr['tstart']).date
        manvr_list.extend([manvr])

    return manvr_list


def read_si_align(char_file):
    """
    Read ODB_SI_ALIGN matrices from supplied characteristics file

    :param char_file: OFLS ODB characteristics file
    :returns: dictionary of matrices, one per detector in original Fortran order
    """
    char_lines = open(char_file).readlines()
    # Find the beginning of the assignment using the regex from aimpoint_mon
    RE_ODB_SI_ALIGN = re.compile(r'\s* ODB_SI_ALIGN \s* =', re.VERBOSE)
    matches = [i for i, line in enumerate(char_lines) if RE_ODB_SI_ALIGN.match(line)]
    if len(matches) != 1:
        raise ValueError('parsing error, matched {} instances of ODB_SI_ALIGN instead of one'
                         .format(len(matches)))
    start = matches[0]
    # Grab the 12 lines of the alignment.  This assumes no extra blank lines
    odb_si_lines = char_lines[start:start+12]
    # Matching the values using a simple comma/space pattern with very little checking
    odb_strings = [list(re.search("(\S+),\s(\S+),\s(\S+),", line).groups()) for line in odb_si_lines]
    odb_floats = np.array(odb_strings).astype(float)
    si_align = {'ACIS-I': odb_floats[0:3],
                'ACIS-S': odb_floats[3:6],
                'HRC-I': odb_floats[6:9],
                'HRC-S': odb_floats[9:12]}
    return si_align
