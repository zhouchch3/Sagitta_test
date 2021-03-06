
NumBlk_weiaddr = 2
NumBlk_flgwei  = 1
NumBlk_wei     = 2
NumBlk_flgact  = 4
NumBlk_act     = 9

CFGCCU_num_layer = 63
CFGCCU_num_patch = 0
CFGCCU_num_ftrgrp= 62
CFGCCU_num_frame = 15
CFGCCU_num_block = 1

CFGGB_num_alloc_flgwei  = NumBlk_flgwei
CFGGB_num_alloc_wei     = NumBlk_wei   
CFGGB_num_alloc_flgact  = NumBlk_flgact
CFGGB_num_alloc_act     = NumBlk_act   

CFGGB_num_total_flgwei = CFGGB_num_alloc_flgwei
CFGGB_num_total_flgact = CFGGB_num_alloc_flgact
CFGGB_num_total_act    = CFGGB_num_alloc_act

CFGGB_num_loop_wei = CFGCCU_num_frame + 1
CFGGB_num_loop_act = CFGCCU_num_ftrgrp + 1

CFGPOOL_data = 8210


group = [ 
        [6, CFGCCU_num_layer],
        [8, CFGCCU_num_patch],
        [11,CFGCCU_num_ftrgrp],
        [6, CFGCCU_num_frame],
        [10,CFGCCU_num_block],

        [4,CFGGB_num_alloc_flgwei],
        [4,CFGGB_num_alloc_wei   ],
        [4,CFGGB_num_alloc_flgact],
        [4,CFGGB_num_alloc_act   ],

        [4,CFGGB_num_total_flgwei],
        [4,CFGGB_num_total_flgact],
        [4,CFGGB_num_total_act   ],

        [12,CFGGB_num_loop_wei],
        [8, CFGGB_num_loop_act],

        [33,CFGPOOL_data]
        ]

def main():
    file = open("ROM.coe", "w")
    file.write("memory_initialization_radix=16;\n")
    file.write("memory_initialization_vector=\n")

    file_sim = open("ROM.txt", "w")

    config_info = ''
    for i in group:
        config_info += dec2width_bin (i[0], i[1])

    # write config
    for i in range(64):
        # 00A01002_18022428_22800804_00002012
        file.write(hex(int(config_info,2)).lstrip('0x').rstrip("L").zfill(32) + ",\n")
        file_sim.write(hex(int(config_info,2)).lstrip('0x').rstrip("L").zfill(32) + "\n")

    # write weiaddr
    file_weiaddr = open("./source_data/addrwei_L00.txt", "r")
    for block in range(NumBlk_weiaddr):
        for i in range(54):
            file_weiaddr, file, file_sim = bin2hex_file(file_weiaddr, file, file_sim)
    # Pad to 64
    for block in range(NumBlk_weiaddr):
        for i in range(10):
            file.write("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" + ",\n")
            file_sim.write("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" + "\n")

    # write weiflag
    file_weiaddr = open("./source_data/flagwei_L00.txt", "r")
    for block in range(NumBlk_flgwei):
        for i in range(512):
            file_weiaddr, file, file_sim = bin2hex_file(file_weiaddr, file, file_sim)

    # write wei 
    file_weiaddr = open("./source_data/datawei_L00.txt", "r")
    for block in range(NumBlk_wei):
        for i in range(512):
            file_weiaddr, file, file_sim = bin2hex_file(file_weiaddr, file, file_sim)

    file_weiaddr = open("./source_data/flagact_L00.txt", "r")
    for block in range(NumBlk_flgact):
        for i in range(512):
            file_weiaddr, file, file_sim = bin2hex_file(file_weiaddr, file, file_sim)

    file_weiaddr = open("./source_data/dataact_L00.txt", "r")
    for block in range(NumBlk_act):
        for i in range(512):
            file_weiaddr, file, file_sim = bin2hex_file(file_weiaddr, file, file_sim)

def bin2hex_file (file_bin, file_hex, file_sim):
    temp = file_bin.readline().rstrip('\n').rstrip('\r')
    # temp = hex(int(temp,2)).lstrip('0x').rstrip("L").zfill(32)

    file_hex.write(temp + ",\n")
    file_sim.write(temp + "\n")
    return file_bin, file_hex, file_sim

def dec2width_bin (width, dec):
    bin_str = bin(dec).lstrip('0b').zfill(width)

    return bin_str

if __name__ == '__main__':
    main()
