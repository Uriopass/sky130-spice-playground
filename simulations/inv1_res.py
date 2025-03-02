import numpy as np
import matplotlib.pyplot as plt

from spice import parse_measures, run_spice

if __name__ == "__main__":
    """ High density """
    capa_hd_inv1       = np.array([0.0005000000, 0.0013351700, 0.0035653300, 0.0095206200, 0.0254232000, 0.0678883000, 0.1812840000])
    cell_fall_hd_inv1  = np.array([0.0143656000, 0.0174314000, 0.0252454000, 0.0454996000, 0.0982781000, 0.2396302000, 0.6168033000]) * 1e-9
    cell_rise_hd_inv1  = np.array([0.0203433000, 0.0255806000, 0.0388749000, 0.0728467000, 0.1628902000, 0.4016502000, 1.0383745000]) * 1e-9
    transition_rise_inv1 = np.array([0.0145424000, 0.0213070000, 0.0395425000, 0.0876798000, 0.2171014000, 0.5586131000, 1.4687663000]) * 1e-9
    transition_fall_inv1 = np.array([0.0078064000, 0.0114862000, 0.0214097000, 0.0477227000, 0.1186008000, 0.3072657000, 0.8034127000]) * 1e-9

    capa_hd_inv2       = np.array([0.0005000000, 0.0014764100, 0.0043595800, 0.0128730000, 0.0380118000, 0.1122420000, 0.3314310000])
    cell_fall_hd_inv2  = np.array([0.0119446000, 0.0137840000, 0.0188149000, 0.0327326000, 0.0729366000, 0.1922578000, 0.5454940000]) * 1e-9
    cell_rise_hd_inv2  = np.array([0.0175587000, 0.0211484000, 0.0310262000, 0.0584472000, 0.1371815000, 0.3662591000, 1.0435811000]) * 1e-9

    capa_hd_inv4       = np.array([0.0005000000, 0.0016127500, 0.0052019300, 0.0167788000, 0.0541202000, 0.1745650000, 0.5630590000])
    cell_fall_hd_inv4  = np.array([0.0119441000, 0.0131118000, 0.0165791000, 0.0269376000, 0.0588054000, 0.1629306000, 0.4909586000]) * 1e-9
    cell_rise_hd_inv4  = np.array([0.0190114000, 0.0215393000, 0.0291288000, 0.0516131000, 0.1202000000, 0.3388957000, 1.0502127000]) * 1e-9

    capa_hd_inv8       = np.array([0.0005000000, 0.0017851100, 0.0063732300, 0.0227538000, 0.0812360000, 0.2900300000, 1.0354700000])
    cell_fall_hd_inv8  = np.array([0.0123297000, 0.0130319000, 0.0154135000, 0.0230701000, 0.0489012000, 0.1402316000, 0.4666703000]) * 1e-9
    cell_rise_hd_inv8  = np.array([0.0202742000, 0.0219295000, 0.0275017000, 0.0455936000, 0.1049458000, 0.3147736000, 1.0550638000]) * 1e-9
    transition_rise_inv8 = np.array([0.0119599000, 0.0138121000, 0.0203450000, 0.0438593000, 0.1268351000, 0.4257829000, 1.4839129000]) * 1e-9
    transition_fall_inv8 = np.array([0.0050158000, 0.0057564000, 0.0084430000, 0.0181318000, 0.0525400000, 0.1754386000, 0.6195076000]) * 1e-9

    capa_hd_inv16      = np.array([0.0005000000, 0.0019354100, 0.0074916000, 0.0289986000, 0.1122480000, 0.4344910000, 1.6818300000])
    cell_fall_hd_inv16 = np.array([0.0152930000, 0.0158333000, 0.0177892000, 0.0242292000, 0.0463429000, 0.1299108000, 0.4538259000]) * 1e-9
    cell_rise_hd_inv16 = np.array([0.0244637000, 0.0256173000, 0.0298987000, 0.0444630000, 0.0949800000, 0.2856741000, 1.0256670000]) * 1e-9
    transition_rise_inv16 = np.array([0.0138044000, 0.0150460000, 0.0198161000, 0.0386202000, 0.1116631000, 0.3939241000, 1.4836817000]) * 1e-9
    transition_fall_inv16 = np.array([0.0065605000, 0.0070460000, 0.0090156000, 0.0170993000, 0.0492442000, 0.1747627000, 0.6592694000]) * 1e-9


    """ High speed """
    capa_hs_inv1 = np.array([0.0000000000, 0.0089400000, 0.0107300000, 0.0128800000, 0.0154500000, 0.0185400000, 0.0222500000, 0.0267000000, 0.0320400000, 0.0384500000, 0.0461400000, 0.0553700000, 0.0664400000, 0.0797300000, 0.0956800000, 0.1148200000, 0.1377900000, 0.1653500000, 0.1984200000, 0.2381100000])
    cell_rise_hs_inv1 = np.array([0.0141400000, 0.0520800000, 0.0594500000, 0.0681800000, 0.0786900000, 0.0912400000, 0.1062000000, 0.1243000000, 0.1458900000, 0.1717000000, 0.2029500000, 0.2403200000, 0.2851700000, 0.3389100000, 0.4033700000, 0.4807900000, 0.5735900000, 0.6848300000, 0.8181800000, 0.9792300000]) * 1e-9
    cell_fall_hs_inv1 = np.array([0.0111600000, 0.0349700000, 0.0395900000, 0.0451300000, 0.0517000000, 0.0595800000, 0.0690900000, 0.0805200000, 0.0941600000, 0.1104500000, 0.1300700000, 0.1537300000, 0.1820800000, 0.2159600000, 0.2567900000, 0.3057500000, 0.3644300000, 0.4343800000, 0.5187300000, 0.6207200000]) * 1e-9

    capa_hs_inv4 = np.array([0.0000000000, 0.0093600000, 0.0112300000, 0.0134700000, 0.0161600000, 0.0193900000, 0.0232700000, 0.0279200000, 0.0335100000, 0.0402100000, 0.0482500000, 0.0579000000, 0.0694800000, 0.0833800000, 0.1000500000, 0.1200600000, 0.1440700000, 0.1728800000, 0.2074500000, 0.2489400000, 0.2987300000, 0.3584700000, 0.4301600000, 0.5161900000, 0.6194300000, 0.7433100000])
    cell_rise_hs_inv4 = np.array([0.0140100000, 0.0275700000, 0.0301500000, 0.0331700000, 0.0367700000, 0.0410500000, 0.0461100000, 0.0522100000, 0.0594300000, 0.0680700000, 0.0784800000, 0.0908800000, 0.1056900000, 0.1233600000, 0.1447000000, 0.1703000000, 0.2009700000, 0.2377400000, 0.2817800000, 0.3345900000, 0.3979500000, 0.4738700000, 0.5655200000, 0.6754000000, 0.8069900000, 0.9645900000]) * 1e-9
    cell_fall_hs_inv4 = np.array([0.0100100000, 0.0170100000, 0.0183000000, 0.0198400000, 0.0216700000, 0.0238500000, 0.0264700000, 0.0295700000, 0.0333000000, 0.0377600000, 0.0430600000, 0.0494700000, 0.0571400000, 0.0663000000, 0.0773100000, 0.0905500000, 0.1063700000, 0.1253100000, 0.1482000000, 0.1757000000, 0.2085400000, 0.2478300000, 0.2949700000, 0.3516500000, 0.4199700000, 0.5019300000]) * 1e-9

    capa_hs_inv16 = np.array([0.0000000000, 0.0068100000, 0.0102100000, 0.0153100000, 0.0229700000, 0.0344600000, 0.0516900000, 0.0775300000, 0.1162900000, 0.1744300000, 0.2616500000, 0.3924700000, 0.5887100000, 0.8830600000, 1.3245900000, 1.8245900000, 2.3245900000, 2.8245900000])
    cell_rise_hs_inv16 = np.array([0.0153200000, 0.0181500000, 0.0195300000, 0.0215500000, 0.0245400000, 0.0289100000, 0.0352800000, 0.0445800000, 0.0583100000, 0.0786400000, 0.1089200000, 0.1539200000, 0.2218600000, 0.3228600000, 0.4751900000, 0.6469000000, 0.8191000000, 0.9915300000]) * 1e-9
    cell_fall_hs_inv16 = np.array([0.0104400000, 0.0117800000, 0.0124200000, 0.0133300000, 0.0146600000, 0.0166000000, 0.0194400000, 0.0236000000, 0.0297700000, 0.0389400000, 0.0526300000, 0.0731400000, 0.1038200000, 0.1500300000, 0.2190300000, 0.2975300000, 0.3754000000, 0.4538800000]) * 1e-9


    inverter_sizes = np.array([1, 4, 16])
    slope_rise = np.zeros_like(inverter_sizes, dtype=np.float64)
    slope_fall = np.zeros_like(inverter_sizes, dtype=np.float64)

    for i, invsize in enumerate(inverter_sizes):
        #t_falls = np.zeros_like(capas)
        capas = np.array(locals()[f"capa_hd_inv{invsize}"])[::2]
        t_rises = np.zeros_like(capas)

        for j,capa in enumerate(capas):
            content = open("inv_1_res.spice").read()
            content = content.replace("{{cval}}", f"{capa}p")
            content = content.replace("{{celltype}}", f"sky130_fd_sc_hd__inv_{invsize}")
            stdout, stderr = run_spice(content)
            measures = parse_measures(stdout)
            if "t_end_rise" not in measures:
                print(stdout)
                print(stderr)
                continue
            #t_fall = measures["t_end_fall"] - measures["t_start_fall"]
            t_rise = measures["t_end_rise"] - measures["t_start_rise"]
            #t_falls[j] = t_fall
            t_rises[j] = t_rise

        print(1e12 * (t_rises[-1] - t_rises[-2]) / (capas[-1] - capas[-2]) * invsize)

        cell_rise_invx = np.array(locals()[f"cell_rise_hd_inv{invsize}"])[::2]
        cell_fall_invx = np.array(locals()[f"cell_fall_hd_inv{invsize}"])[::2]

        #transition_rise_invx = np.array(locals()[f"transition_rise_inv{invsize}"])
        #transition_fall_invx = np.array(locals()[f"transition_fall_inv{invsize}"])

        plt.plot(capas, ((t_rises - t_rises[0]) * invsize), label=f"rise_{invsize}", marker="o")

        #plt.plot(capas, (transition_fall_invx - transition_fall_invx[0]) * invsize, label=f"rise_{invsize}_ref", marker="x", linestyle="--")

        plt.plot(capas, (cell_rise_invx - cell_rise_invx[0]) * invsize, label=f"rise_{invsize}_ref", marker="x", linestyle="--")
        #plt.plot(capas, (cell_fall_invx - cell_fall_invx[0]) * invsize, label=f"rise_{invsize}_ref", marker="x", linestyle="--")

        print(invsize, cell_rise_invx[-1] / t_rises[-1])

        #slope_rise[i] = (cell_rise_invx[-1] - cell_rise_invx[-2]) / (capas[-1] - capas[-2])
        #slope_fall[i] = (cell_fall_invx[-1] - cell_fall_invx[-2]) / (capas[-1] - capas[-2])

    print(slope_rise)

    plt.xlabel("Capacitance (pF)")
    plt.ylabel("Delay (s)")
    plt.gca().yaxis.label.set(rotation='horizontal', ha='right')

    #plt.plot(inverter_sizes, slope_rise, label="rise", marker="o")
    #plt.plot(inverter_sizes, slope_rise[0] / inverter_sizes, label="rise_ideal", marker="x", linestyle="--")
    #plt.plot(inverter_sizes, slope_fall, label="fall", marker="o")
    #plt.plot(inverter_sizes, slope_fall[0] / inverter_sizes, label="fall_ideal", marker="x", linestyle="--")
    #plt.xlabel("Inverter size")
    #plt.ylabel("Slope (s/pF)")

    #plt.legend()
    #plt.show()

    plt.legend()
    plt.show()