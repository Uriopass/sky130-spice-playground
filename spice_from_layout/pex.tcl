
    # read design
    gds read sky130_fd_sc_hs.gds
    
    extract path ext
    
    ext2spice lvs
    ext2spice cthresh 0
    ext2spice rthresh 0
    ext2spice extresist on
    ext2spice subcircuit on
    ext2spice ngspice
    
    
    load sky130_fd_sc_hs__inv_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__inv_1.spice
    

    load sky130_fd_sc_hs__inv_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__inv_2.spice
    

    load sky130_fd_sc_hs__inv_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__inv_4.spice
    

    load sky130_fd_sc_hs__inv_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__inv_8.spice
    

    load sky130_fd_sc_hs__inv_16
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__inv_16.spice
    

    load sky130_fd_sc_hs__sdfrbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfrbp_2.spice
    

    load sky130_fd_sc_hs__sdfxbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfxbp_2.spice
    

    load sky130_fd_sc_hs__sdfxbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfxbp_1.spice
    

    load sky130_fd_sc_hs__sdfstp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfstp_4.spice
    

    load sky130_fd_sc_hs__sdfstp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfstp_2.spice
    

    load sky130_fd_sc_hs__sdfstp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfstp_1.spice
    

    load sky130_fd_sc_hs__sdfsbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfsbp_2.spice
    

    load sky130_fd_sc_hs__sdfsbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfsbp_1.spice
    

    load sky130_fd_sc_hs__sdfrtp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfrtp_4.spice
    

    load sky130_fd_sc_hs__sdfrtp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfrtp_2.spice
    

    load sky130_fd_sc_hs__sdfrtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfrtp_1.spice
    

    load sky130_fd_sc_hs__sdfrtn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfrtn_1.spice
    

    load sky130_fd_sc_hs__sdlclkp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdlclkp_1.spice
    

    load sky130_fd_sc_hs__sdlclkp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdlclkp_2.spice
    

    load sky130_fd_sc_hs__sdfxtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfxtp_1.spice
    

    load sky130_fd_sc_hs__sdfxtp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfxtp_2.spice
    

    load sky130_fd_sc_hs__sdfxtp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfxtp_4.spice
    

    load sky130_fd_sc_hs__sdlclkp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdlclkp_4.spice
    

    load sky130_fd_sc_hs__sedfxbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sedfxbp_1.spice
    

    load sky130_fd_sc_hs__sedfxbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sedfxbp_2.spice
    

    load sky130_fd_sc_hs__sedfxtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sedfxtp_1.spice
    

    load sky130_fd_sc_hs__sedfxtp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sedfxtp_2.spice
    

    load sky130_fd_sc_hs__xnor2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xnor2_4.spice
    

    load sky130_fd_sc_hs__xnor2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xnor2_2.spice
    

    load sky130_fd_sc_hs__xnor2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xnor2_1.spice
    

    load sky130_fd_sc_hs__tapvpwrvgnd_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__tapvpwrvgnd_1.spice
    

    load sky130_fd_sc_hs__tapvgnd_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__tapvgnd_1.spice
    

    load sky130_fd_sc_hs__tapvgnd2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__tapvgnd2_1.spice
    

    load sky130_fd_sc_hs__tapmet1_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__tapmet1_2.spice
    

    load sky130_fd_sc_hs__tap_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__tap_2.spice
    

    load sky130_fd_sc_hs__tap_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__tap_1.spice
    

    load sky130_fd_sc_hs__sedfxtp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sedfxtp_4.spice
    

    load sky130_fd_sc_hs__xnor3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xnor3_1.spice
    

    load sky130_fd_sc_hs__xnor3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xnor3_2.spice
    

    load sky130_fd_sc_hs__xnor3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xnor3_4.spice
    

    load sky130_fd_sc_hs__xor2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xor2_1.spice
    

    load sky130_fd_sc_hs__xor2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xor2_2.spice
    

    load sky130_fd_sc_hs__xor2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xor2_4.spice
    

    load sky130_fd_sc_hs__xor3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xor3_1.spice
    

    load sky130_fd_sc_hs__xor3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xor3_2.spice
    

    load sky130_fd_sc_hs__xor3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__xor3_4.spice
    

    load sky130_fd_sc_hs__o2111a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2111a_1.spice
    

    load sky130_fd_sc_hs__o311ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o311ai_4.spice
    

    load sky130_fd_sc_hs__o311ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o311ai_2.spice
    

    load sky130_fd_sc_hs__o311ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o311ai_1.spice
    

    load sky130_fd_sc_hs__o311a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o311a_4.spice
    

    load sky130_fd_sc_hs__o311a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o311a_2.spice
    

    load sky130_fd_sc_hs__o311a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o311a_1.spice
    

    load sky130_fd_sc_hs__o221ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o221ai_4.spice
    

    load sky130_fd_sc_hs__o221ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o221ai_2.spice
    

    load sky130_fd_sc_hs__o221ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o221ai_1.spice
    

    load sky130_fd_sc_hs__o2111a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2111a_2.spice
    

    load sky130_fd_sc_hs__o2111a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2111a_4.spice
    

    load sky130_fd_sc_hs__o2111ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2111ai_1.spice
    

    load sky130_fd_sc_hs__o2111ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2111ai_2.spice
    

    load sky130_fd_sc_hs__or2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or2_1.spice
    

    load sky130_fd_sc_hs__or2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or2_2.spice
    

    load sky130_fd_sc_hs__or2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or2_4.spice
    

    load sky130_fd_sc_hs__or2b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or2b_1.spice
    

    load sky130_fd_sc_hs__or2b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or2b_2.spice
    

    load sky130_fd_sc_hs__or2b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or2b_4.spice
    

    load sky130_fd_sc_hs__o2111ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2111ai_4.spice
    

    load sky130_fd_sc_hs__or3b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or3b_1.spice
    

    load sky130_fd_sc_hs__or4_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4_2.spice
    

    load sky130_fd_sc_hs__or4_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4_1.spice
    

    load sky130_fd_sc_hs__or3b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or3b_4.spice
    

    load sky130_fd_sc_hs__or3b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or3b_2.spice
    

    load sky130_fd_sc_hs__or4b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4b_1.spice
    

    load sky130_fd_sc_hs__or4_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4_4.spice
    

    load sky130_fd_sc_hs__or3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or3_4.spice
    

    load sky130_fd_sc_hs__or3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or3_2.spice
    

    load sky130_fd_sc_hs__or3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or3_1.spice
    

    load sky130_fd_sc_hs__or4b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4b_2.spice
    

    load sky130_fd_sc_hs__or4b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4b_4.spice
    

    load sky130_fd_sc_hs__or4bb_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4bb_1.spice
    

    load sky130_fd_sc_hs__or4bb_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4bb_2.spice
    

    load sky130_fd_sc_hs__or4bb_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__or4bb_4.spice
    

    load sky130_fd_sc_hs__sdfbbn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfbbn_1.spice
    

    load sky130_fd_sc_hs__sdfbbn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfbbn_2.spice
    

    load sky130_fd_sc_hs__sdfbbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfbbp_1.spice
    

    load sky130_fd_sc_hs__sdfrbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__sdfrbp_1.spice
    

    load sky130_fd_sc_hs__o22a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o22a_2.spice
    

    load sky130_fd_sc_hs__o21ba_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21ba_2.spice
    

    load sky130_fd_sc_hs__o21ba_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21ba_1.spice
    

    load sky130_fd_sc_hs__o21ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21ai_4.spice
    

    load sky130_fd_sc_hs__o21ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21ai_2.spice
    

    load sky130_fd_sc_hs__o21bai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21bai_4.spice
    

    load sky130_fd_sc_hs__o21bai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21bai_2.spice
    

    load sky130_fd_sc_hs__o21bai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21bai_1.spice
    

    load sky130_fd_sc_hs__o21ba_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21ba_4.spice
    

    load sky130_fd_sc_hs__o22a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o22a_1.spice
    

    load sky130_fd_sc_hs__o31a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o31a_1.spice
    

    load sky130_fd_sc_hs__o22ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o22ai_4.spice
    

    load sky130_fd_sc_hs__o22ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o22ai_2.spice
    

    load sky130_fd_sc_hs__o22ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o22ai_1.spice
    

    load sky130_fd_sc_hs__o22a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o22a_4.spice
    

    load sky130_fd_sc_hs__o31ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o31ai_4.spice
    

    load sky130_fd_sc_hs__o31ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o31ai_2.spice
    

    load sky130_fd_sc_hs__o31ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o31ai_1.spice
    

    load sky130_fd_sc_hs__o31a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o31a_4.spice
    

    load sky130_fd_sc_hs__o31a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o31a_2.spice
    

    load sky130_fd_sc_hs__o32a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o32a_1.spice
    

    load sky130_fd_sc_hs__o41ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o41ai_2.spice
    

    load sky130_fd_sc_hs__o41ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o41ai_1.spice
    

    load sky130_fd_sc_hs__o41a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o41a_4.spice
    

    load sky130_fd_sc_hs__o41a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o41a_2.spice
    

    load sky130_fd_sc_hs__o41a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o41a_1.spice
    

    load sky130_fd_sc_hs__o32ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o32ai_4.spice
    

    load sky130_fd_sc_hs__o32ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o32ai_2.spice
    

    load sky130_fd_sc_hs__o32ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o32ai_1.spice
    

    load sky130_fd_sc_hs__o32a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o32a_4.spice
    

    load sky130_fd_sc_hs__o32a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o32a_2.spice
    

    load sky130_fd_sc_hs__o211a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o211a_1.spice
    

    load sky130_fd_sc_hs__o211a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o211a_2.spice
    

    load sky130_fd_sc_hs__o211a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o211a_4.spice
    

    load sky130_fd_sc_hs__o211ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o211ai_1.spice
    

    load sky130_fd_sc_hs__o211ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o211ai_2.spice
    

    load sky130_fd_sc_hs__o211ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o211ai_4.spice
    

    load sky130_fd_sc_hs__o221a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o221a_1.spice
    

    load sky130_fd_sc_hs__o221a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o221a_2.spice
    

    load sky130_fd_sc_hs__o221a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o221a_4.spice
    

    load sky130_fd_sc_hs__o41ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o41ai_4.spice
    

    load sky130_fd_sc_hs__nand4_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4_2.spice
    

    load sky130_fd_sc_hs__nand4_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4_4.spice
    

    load sky130_fd_sc_hs__nand4b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4b_1.spice
    

    load sky130_fd_sc_hs__nand4b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4b_2.spice
    

    load sky130_fd_sc_hs__nand4b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4b_4.spice
    

    load sky130_fd_sc_hs__nand4bb_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4bb_1.spice
    

    load sky130_fd_sc_hs__nand4bb_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4bb_2.spice
    

    load sky130_fd_sc_hs__nand4bb_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4bb_4.spice
    

    load sky130_fd_sc_hs__nor2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2_1.spice
    

    load sky130_fd_sc_hs__nor2b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2b_2.spice
    

    load sky130_fd_sc_hs__nor2b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2b_1.spice
    

    load sky130_fd_sc_hs__nor2_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2_8.spice
    

    load sky130_fd_sc_hs__nor2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2_4.spice
    

    load sky130_fd_sc_hs__nor2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2_2.spice
    

    load sky130_fd_sc_hs__nor3b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor3b_1.spice
    

    load sky130_fd_sc_hs__nor3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor3_4.spice
    

    load sky130_fd_sc_hs__nor3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor3_2.spice
    

    load sky130_fd_sc_hs__nor3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor3_1.spice
    

    load sky130_fd_sc_hs__nor2b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor2b_4.spice
    

    load sky130_fd_sc_hs__nor4bb_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4bb_4.spice
    

    load sky130_fd_sc_hs__nor4bb_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4bb_2.spice
    

    load sky130_fd_sc_hs__nor4bb_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4bb_1.spice
    

    load sky130_fd_sc_hs__nor4b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4b_4.spice
    

    load sky130_fd_sc_hs__nor4b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4b_2.spice
    

    load sky130_fd_sc_hs__nor4b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4b_1.spice
    

    load sky130_fd_sc_hs__nor4_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4_4.spice
    

    load sky130_fd_sc_hs__nor4_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4_2.spice
    

    load sky130_fd_sc_hs__nor4_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor4_1.spice
    

    load sky130_fd_sc_hs__nor3b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor3b_4.spice
    

    load sky130_fd_sc_hs__nor3b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nor3b_2.spice
    

    load sky130_fd_sc_hs__o2bb2a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2bb2a_1.spice
    

    load sky130_fd_sc_hs__o2bb2a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2bb2a_2.spice
    

    load sky130_fd_sc_hs__o2bb2a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2bb2a_4.spice
    

    load sky130_fd_sc_hs__o2bb2ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2bb2ai_1.spice
    

    load sky130_fd_sc_hs__o2bb2ai_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2bb2ai_2.spice
    

    load sky130_fd_sc_hs__o21a_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21a_1.spice
    

    load sky130_fd_sc_hs__o21a_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21a_2.spice
    

    load sky130_fd_sc_hs__o21a_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21a_4.spice
    

    load sky130_fd_sc_hs__o21ai_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o21ai_1.spice
    

    load sky130_fd_sc_hs__o2bb2ai_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__o2bb2ai_4.spice
    

    load sky130_fd_sc_hs__fill_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_1.spice
    

    load sky130_fd_sc_hs__fill_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_2.spice
    

    load sky130_fd_sc_hs__fill_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_4.spice
    

    load sky130_fd_sc_hs__fill_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_8.spice
    

    load sky130_fd_sc_hs__fill_diode_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_diode_2.spice
    

    load sky130_fd_sc_hs__fill_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_2.spice
    

    load sky130_fd_sc_hs__fill_diode_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_diode_4.spice
    

    load sky130_fd_sc_hs__fill_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_4.spice
    

    load sky130_fd_sc_hs__fill_diode_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_diode_8.spice
    

    load sky130_fd_sc_hs__fill_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fill_8.spice
    

    load sky130_fd_sc_hs__ha_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ha_1.spice
    

    load sky130_fd_sc_hs__ha_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ha_2.spice
    

    load sky130_fd_sc_hs__maj3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__maj3_1.spice
    

    load sky130_fd_sc_hs__maj3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__maj3_2.spice
    

    load sky130_fd_sc_hs__maj3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__maj3_4.spice
    

    load sky130_fd_sc_hs__mux2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux2_1.spice
    

    load sky130_fd_sc_hs__ha_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ha_4.spice
    

    load sky130_fd_sc_hs__nand2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2_4.spice
    

    load sky130_fd_sc_hs__nand2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2_2.spice
    

    load sky130_fd_sc_hs__nand2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2_1.spice
    

    load sky130_fd_sc_hs__mux4_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux4_4.spice
    

    load sky130_fd_sc_hs__mux4_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux4_2.spice
    

    load sky130_fd_sc_hs__mux4_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux4_1.spice
    

    load sky130_fd_sc_hs__mux2i_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux2i_4.spice
    

    load sky130_fd_sc_hs__mux2i_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux2i_2.spice
    

    load sky130_fd_sc_hs__mux2i_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux2i_1.spice
    

    load sky130_fd_sc_hs__mux2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux2_4.spice
    

    load sky130_fd_sc_hs__mux2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__mux2_2.spice
    

    load sky130_fd_sc_hs__nand2b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2b_4.spice
    

    load sky130_fd_sc_hs__nand2b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2b_2.spice
    

    load sky130_fd_sc_hs__nand2b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2b_1.spice
    

    load sky130_fd_sc_hs__nand2_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand2_8.spice
    

    load sky130_fd_sc_hs__nand3b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand3b_2.spice
    

    load sky130_fd_sc_hs__nand3b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand3b_1.spice
    

    load sky130_fd_sc_hs__nand3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand3_4.spice
    

    load sky130_fd_sc_hs__nand3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand3_2.spice
    

    load sky130_fd_sc_hs__nand3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand3_1.spice
    

    load sky130_fd_sc_hs__nand3b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand3b_4.spice
    

    load sky130_fd_sc_hs__nand4_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__nand4_1.spice
    

    load sky130_fd_sc_hs__dlrtn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrtn_2.spice
    

    load sky130_fd_sc_hs__dlrtn_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrtn_4.spice
    

    load sky130_fd_sc_hs__dlrtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrtp_1.spice
    

    load sky130_fd_sc_hs__dlrtp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrtp_2.spice
    

    load sky130_fd_sc_hs__dlrtp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrtp_4.spice
    

    load sky130_fd_sc_hs__dlxbn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxbn_1.spice
    

    load sky130_fd_sc_hs__dlxbn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxbn_2.spice
    

    load sky130_fd_sc_hs__dlxbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxbp_1.spice
    

    load sky130_fd_sc_hs__dlygate4sd1_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlygate4sd1_1.spice
    

    load sky130_fd_sc_hs__dlxtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxtp_1.spice
    

    load sky130_fd_sc_hs__dlxtn_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxtn_4.spice
    

    load sky130_fd_sc_hs__dlxtn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxtn_2.spice
    

    load sky130_fd_sc_hs__dlymetal6s4s_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlymetal6s4s_1.spice
    

    load sky130_fd_sc_hs__dlymetal6s2s_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlymetal6s2s_1.spice
    

    load sky130_fd_sc_hs__dlygate4sd3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlygate4sd3_1.spice
    

    load sky130_fd_sc_hs__dlygate4sd2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlygate4sd2_1.spice
    

    load sky130_fd_sc_hs__dlymetal6s6s_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlymetal6s6s_1.spice
    

    load sky130_fd_sc_hs__dlxtn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlxtn_1.spice
    

    load sky130_fd_sc_hs__einvn_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvn_8.spice
    

    load sky130_fd_sc_hs__einvn_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvn_4.spice
    

    load sky130_fd_sc_hs__einvn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvn_2.spice
    

    load sky130_fd_sc_hs__einvn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvn_1.spice
    

    load sky130_fd_sc_hs__edfxtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__edfxtp_1.spice
    

    load sky130_fd_sc_hs__edfxbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__edfxbp_1.spice
    

    load sky130_fd_sc_hs__ebufn_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ebufn_8.spice
    

    load sky130_fd_sc_hs__ebufn_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ebufn_4.spice
    

    load sky130_fd_sc_hs__ebufn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ebufn_2.spice
    

    load sky130_fd_sc_hs__ebufn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__ebufn_1.spice
    

    load sky130_fd_sc_hs__einvp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvp_1.spice
    

    load sky130_fd_sc_hs__einvp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvp_2.spice
    

    load sky130_fd_sc_hs__einvp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvp_4.spice
    

    load sky130_fd_sc_hs__fa_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fa_1.spice
    

    load sky130_fd_sc_hs__einvp_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__einvp_8.spice
    

    load sky130_fd_sc_hs__fa_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fa_2.spice
    

    load sky130_fd_sc_hs__fa_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fa_4.spice
    

    load sky130_fd_sc_hs__fah_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fah_1.spice
    

    load sky130_fd_sc_hs__fah_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fah_2.spice
    

    load sky130_fd_sc_hs__fah_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fah_4.spice
    

    load sky130_fd_sc_hs__fahcin_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fahcin_1.spice
    

    load sky130_fd_sc_hs__fahcon_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__fahcon_1.spice
    

    load sky130_fd_sc_hs__clkdlyinv3sd2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkdlyinv3sd2_1.spice
    

    load sky130_fd_sc_hs__clkdlyinv3sd3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkdlyinv3sd3_1.spice
    

    load sky130_fd_sc_hs__clkdlyinv5sd1_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkdlyinv5sd1_1.spice
    

    load sky130_fd_sc_hs__clkdlyinv5sd2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkdlyinv5sd2_1.spice
    

    load sky130_fd_sc_hs__clkdlyinv5sd3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkdlyinv5sd3_1.spice
    

    load sky130_fd_sc_hs__clkinv_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkinv_1.spice
    

    load sky130_fd_sc_hs__clkinv_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkinv_2.spice
    

    load sky130_fd_sc_hs__clkinv_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkinv_4.spice
    

    load sky130_fd_sc_hs__dfrbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfrbp_2.spice
    

    load sky130_fd_sc_hs__dfrbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfrbp_1.spice
    

    load sky130_fd_sc_hs__dfbbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfbbp_1.spice
    

    load sky130_fd_sc_hs__dfbbn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfbbn_2.spice
    

    load sky130_fd_sc_hs__dfbbn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfbbn_1.spice
    

    load sky130_fd_sc_hs__decap_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__decap_8.spice
    

    load sky130_fd_sc_hs__decap_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__decap_4.spice
    

    load sky130_fd_sc_hs__conb_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__conb_1.spice
    

    load sky130_fd_sc_hs__clkinv_16
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkinv_16.spice
    

    load sky130_fd_sc_hs__clkinv_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkinv_8.spice
    

    load sky130_fd_sc_hs__dfxbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfxbp_1.spice
    

    load sky130_fd_sc_hs__dfstp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfstp_4.spice
    

    load sky130_fd_sc_hs__dfstp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfstp_2.spice
    

    load sky130_fd_sc_hs__dfstp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfstp_1.spice
    

    load sky130_fd_sc_hs__dfsbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfsbp_2.spice
    

    load sky130_fd_sc_hs__dfsbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfsbp_1.spice
    

    load sky130_fd_sc_hs__dfrtp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfrtp_4.spice
    

    load sky130_fd_sc_hs__dfrtp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfrtp_2.spice
    

    load sky130_fd_sc_hs__dfrtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfrtp_1.spice
    

    load sky130_fd_sc_hs__dfrtn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfrtn_1.spice
    

    load sky130_fd_sc_hs__dfxtp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfxtp_1.spice
    

    load sky130_fd_sc_hs__dfxtp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfxtp_2.spice
    

    load sky130_fd_sc_hs__diode_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__diode_2.spice
    

    load sky130_fd_sc_hs__dlclkp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlclkp_1.spice
    

    load sky130_fd_sc_hs__dlclkp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlclkp_2.spice
    

    load sky130_fd_sc_hs__dlclkp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlclkp_4.spice
    

    load sky130_fd_sc_hs__dlrbn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrbn_1.spice
    

    load sky130_fd_sc_hs__dlrbp_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrbp_1.spice
    

    load sky130_fd_sc_hs__dfxbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfxbp_2.spice
    

    load sky130_fd_sc_hs__dfxtp_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dfxtp_4.spice
    

    load sky130_fd_sc_hs__dlrbn_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrbn_2.spice
    

    load sky130_fd_sc_hs__dlrbp_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrbp_2.spice
    

    load sky130_fd_sc_hs__dlrtn_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__dlrtn_1.spice
    

    load sky130_fd_sc_hs__a2111o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2111o_4.spice
    

    load sky130_fd_sc_hs__a2111oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2111oi_1.spice
    

    load sky130_fd_sc_hs__a2111oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2111oi_2.spice
    

    load sky130_fd_sc_hs__a2111oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2111oi_4.spice
    

    load sky130_fd_sc_hs__and2_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and2_1.spice
    

    load sky130_fd_sc_hs__and2_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and2_2.spice
    

    load sky130_fd_sc_hs__and2_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and2_4.spice
    

    load sky130_fd_sc_hs__and2b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and2b_4.spice
    

    load sky130_fd_sc_hs__and3b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and3b_1.spice
    

    load sky130_fd_sc_hs__and3_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and3_4.spice
    

    load sky130_fd_sc_hs__and3_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and3_2.spice
    

    load sky130_fd_sc_hs__and3_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and3_1.spice
    

    load sky130_fd_sc_hs__and4_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4_1.spice
    

    load sky130_fd_sc_hs__and3b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and3b_4.spice
    

    load sky130_fd_sc_hs__and3b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and3b_2.spice
    

    load sky130_fd_sc_hs__and2b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and2b_2.spice
    

    load sky130_fd_sc_hs__and2b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and2b_1.spice
    

    load sky130_fd_sc_hs__buf_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__buf_2.spice
    

    load sky130_fd_sc_hs__buf_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__buf_1.spice
    

    load sky130_fd_sc_hs__and4bb_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4bb_4.spice
    

    load sky130_fd_sc_hs__and4bb_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4bb_2.spice
    

    load sky130_fd_sc_hs__and4bb_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4bb_1.spice
    

    load sky130_fd_sc_hs__and4b_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4b_4.spice
    

    load sky130_fd_sc_hs__and4b_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4b_2.spice
    

    load sky130_fd_sc_hs__and4b_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4b_1.spice
    

    load sky130_fd_sc_hs__and4_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4_4.spice
    

    load sky130_fd_sc_hs__and4_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__and4_2.spice
    

    load sky130_fd_sc_hs__buf_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__buf_4.spice
    

    load sky130_fd_sc_hs__buf_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__buf_8.spice
    

    load sky130_fd_sc_hs__bufbuf_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__bufbuf_8.spice
    

    load sky130_fd_sc_hs__bufinv_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__bufinv_8.spice
    

    load sky130_fd_sc_hs__clkbuf_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkbuf_1.spice
    

    load sky130_fd_sc_hs__clkbuf_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkbuf_2.spice
    

    load sky130_fd_sc_hs__clkbuf_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkbuf_4.spice
    

    load sky130_fd_sc_hs__buf_16
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__buf_16.spice
    

    load sky130_fd_sc_hs__bufbuf_16
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__bufbuf_16.spice
    

    load sky130_fd_sc_hs__bufinv_16
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__bufinv_16.spice
    

    load sky130_fd_sc_hs__clkbuf_8
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkbuf_8.spice
    

    load sky130_fd_sc_hs__clkbuf_16
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkbuf_16.spice
    

    load sky130_fd_sc_hs__clkdlyinv3sd1_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__clkdlyinv3sd1_1.spice
    

    load sky130_fd_sc_hs__a31o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a31o_2.spice
    

    load sky130_fd_sc_hs__a31o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a31o_4.spice
    

    load sky130_fd_sc_hs__a31oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a31oi_1.spice
    

    load sky130_fd_sc_hs__a31oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a31oi_2.spice
    

    load sky130_fd_sc_hs__a31oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a31oi_4.spice
    

    load sky130_fd_sc_hs__a32o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a32o_1.spice
    

    load sky130_fd_sc_hs__a41oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a41oi_4.spice
    

    load sky130_fd_sc_hs__a41oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a41oi_2.spice
    

    load sky130_fd_sc_hs__a41oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a41oi_1.spice
    

    load sky130_fd_sc_hs__a41o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a41o_4.spice
    

    load sky130_fd_sc_hs__a41o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a41o_2.spice
    

    load sky130_fd_sc_hs__a41o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a41o_1.spice
    

    load sky130_fd_sc_hs__a32oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a32oi_4.spice
    

    load sky130_fd_sc_hs__a32oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a32oi_2.spice
    

    load sky130_fd_sc_hs__a32oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a32oi_1.spice
    

    load sky130_fd_sc_hs__a32o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a32o_4.spice
    

    load sky130_fd_sc_hs__a32o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a32o_2.spice
    

    load sky130_fd_sc_hs__a221oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a221oi_1.spice
    

    load sky130_fd_sc_hs__a221o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a221o_4.spice
    

    load sky130_fd_sc_hs__a221o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a221o_2.spice
    

    load sky130_fd_sc_hs__a221o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a221o_1.spice
    

    load sky130_fd_sc_hs__a211oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a211oi_4.spice
    

    load sky130_fd_sc_hs__a211oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a211oi_2.spice
    

    load sky130_fd_sc_hs__a211oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a211oi_1.spice
    

    load sky130_fd_sc_hs__a211o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a211o_4.spice
    

    load sky130_fd_sc_hs__a211o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a211o_2.spice
    

    load sky130_fd_sc_hs__a211o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a211o_1.spice
    

    load sky130_fd_sc_hs__a221oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a221oi_2.spice
    

    load sky130_fd_sc_hs__a222o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a222o_1.spice
    

    load sky130_fd_sc_hs__a222o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a222o_2.spice
    

    load sky130_fd_sc_hs__a222oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a222oi_1.spice
    

    load sky130_fd_sc_hs__a222oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a222oi_2.spice
    

    load sky130_fd_sc_hs__a311o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a311o_1.spice
    

    load sky130_fd_sc_hs__a311o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a311o_2.spice
    

    load sky130_fd_sc_hs__a311o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a311o_4.spice
    

    load sky130_fd_sc_hs__a311oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a311oi_1.spice
    

    load sky130_fd_sc_hs__a221oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a221oi_4.spice
    

    load sky130_fd_sc_hs__a311oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a311oi_2.spice
    

    load sky130_fd_sc_hs__a311oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a311oi_4.spice
    

    load sky130_fd_sc_hs__a2111o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2111o_1.spice
    

    load sky130_fd_sc_hs__a2111o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2111o_2.spice
    

    load sky130_fd_sc_hs__a21boi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21boi_2.spice
    

    load sky130_fd_sc_hs__a2bb2oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2bb2oi_2.spice
    

    load sky130_fd_sc_hs__a2bb2oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2bb2oi_1.spice
    

    load sky130_fd_sc_hs__a2bb2o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2bb2o_4.spice
    

    load sky130_fd_sc_hs__a2bb2o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2bb2o_2.spice
    

    load sky130_fd_sc_hs__a2bb2o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2bb2o_1.spice
    

    load sky130_fd_sc_hs__a21boi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21boi_1.spice
    

    load sky130_fd_sc_hs__a21bo_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21bo_4.spice
    

    load sky130_fd_sc_hs__a21bo_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21bo_2.spice
    

    load sky130_fd_sc_hs__a21bo_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21bo_1.spice
    

    load sky130_fd_sc_hs__a2bb2oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a2bb2oi_4.spice
    

    load sky130_fd_sc_hs__a21o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21o_4.spice
    

    load sky130_fd_sc_hs__a21o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21o_2.spice
    

    load sky130_fd_sc_hs__a21o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21o_1.spice
    

    load sky130_fd_sc_hs__a21boi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21boi_4.spice
    

    load sky130_fd_sc_hs__a22o_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a22o_2.spice
    

    load sky130_fd_sc_hs__a22o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a22o_1.spice
    

    load sky130_fd_sc_hs__a21oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21oi_4.spice
    

    load sky130_fd_sc_hs__a21oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21oi_2.spice
    

    load sky130_fd_sc_hs__a21oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a21oi_1.spice
    

    load sky130_fd_sc_hs__a22o_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a22o_4.spice
    

    load sky130_fd_sc_hs__a22oi_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a22oi_1.spice
    

    load sky130_fd_sc_hs__a22oi_2
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a22oi_2.spice
    

    load sky130_fd_sc_hs__a22oi_4
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a22oi_4.spice
    

    load sky130_fd_sc_hs__a31o_1
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/sky130_fd_sc_hs__a31o_1.spice
    
    
    # quit
    quit
    