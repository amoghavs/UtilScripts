#! /bin/bash

#Average=(17 10 24 38 24 10 45 10 24 38 52 66 31 73 38 38 31 80 38 66 101 87 101 73 80 87 52)
# Energy=(21 13 29 45 29 13 53 13 29 45 61 77 37 85 45 45 37 93 45 77 117 101 117 85 93 101 61)
# ParamStart=( 32 19 43 63 43 21 76 21 43 63 86 109 54 120 65 65 53 130 65 109 163 141 162 120 131 142 86 )
# FreqParam=( 41 23 55 79 55 27 97 27 55 79 109 139 69 153 83 83 67 165 83 139 207 179 205 153 167 181 109 )
# NumLines=(44 26 59 85 59 29 104 29 59 85 117 149 74 164 89 89 72 177 89 149 222 192 220 164 179 1 195 117)
 
declare -a Stop=( 41 23 55 79 55 27 97 27 55 79 109 139 69 153 83 83 67 165 83 139 207 179 205 153 167 181 109 )
declare -a Start=( 32 19 43 63 43 21 76 21 43 63 86 109 54 120 65 65 53 130 65 109 163 141 162 120 131 142 86 )
 Files=(
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PP_Iters_181_OpsLength_2_Random_0_Dims_1_DS_d_Size_2097152.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PP_Iters_2000000_OpsLength_2_Random_0_Dims_1_DS_d_Size_1024.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PP_Iters_3971641_OpsLength_2_Random_0_Dims_1_DS_d_Size_1024.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PP_Iters_397164_OpsLength_2_Random_0_Dims_1_DS_d_Size_8192.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PppPpp_Iters_1985820_OpsLength_4_Random_0_Dims_1_DS_d_Size_1024.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PppPpp_Iters_198582_OpsLength_4_Random_0_Dims_1_DS_d_Size_8192.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PppPpp_Iters_90_OpsLength_4_Random_0_Dims_1_DS_d_Size_2097152.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PppppppPpppppp_Iters_45_OpsLength_8_Random_0_Dims_1_DS_d_Size_2097152.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PppppppPpppppp_Iters_992910_OpsLength_8_Random_0_Dims_1_DS_d_Size_1024.log'
'Stats_Alloc_d_Stream_2_Vars_1_Ops_PppppppPpppppp_Iters_99291_OpsLength_8_Random_0_Dims_1_DS_d_Size_8192.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PPP_Iters_121_OpsLength_2_Random_0_Dims_1_DS_d_Size_1048576.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PPP_Iters_2647760_OpsLength_2_Random_0_Dims_1_DS_d_Size_512.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PPP_Iters_264776_OpsLength_2_Random_0_Dims_1_DS_d_Size_4096.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PppPppPpp_Iters_1323880_OpsLength_4_Random_0_Dims_1_DS_d_Size_512.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PppPppPpp_Iters_132388_OpsLength_4_Random_0_Dims_1_DS_d_Size_4096.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PppPppPpp_Iters_60_OpsLength_4_Random_0_Dims_1_DS_d_Size_1048576.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PppppppPppppppPpppppp_Iters_30_OpsLength_8_Random_0_Dims_1_DS_d_Size_1048576.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PppppppPppppppPpppppp_Iters_661940_OpsLength_8_Random_0_Dims_1_DS_d_Size_512.log'
'Stats_Alloc_d_Stream_3_Vars_1_Ops_PppppppPppppppPpppppp_Iters_66194_OpsLength_8_Random_0_Dims_1_DS_d_Size_4096.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PPPP_Iters_1985820_OpsLength_2_Random_0_Dims_1_DS_d_Size_512.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PPPP_Iters_198582_OpsLength_2_Random_0_Dims_1_DS_d_Size_4096.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PPPP_Iters_90_OpsLength_2_Random_0_Dims_1_DS_d_Size_1048576.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PppPppPppPpp_Iters_45_OpsLength_4_Random_0_Dims_1_DS_d_Size_1048576.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PppPppPppPpp_Iters_992910_OpsLength_4_Random_0_Dims_1_DS_d_Size_512.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PppPppPppPpp_Iters_99291_OpsLength_4_Random_0_Dims_1_DS_d_Size_4096.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PppppppPppppppPppppppPpppppp_Iters_496455_OpsLength_8_Random_0_Dims_1_DS_d_Size_512.log'
'Stats_Alloc_d_Stream_4_Vars_1_Ops_PppppppPppppppPppppppPpppppp_Iters_49645_OpsLength_8_Random_0_Dims_1_DS_d_Size_4096.log')

StartIdx=1
IncrementIdx=1
OutputFileName='Rapl.log' #'AverageRunTime.log'
NumFiles=27
`rm -f Meh.log`
for ((i=0;i<$NumFiles ; i++))
do 
	echo " Start: ${Start[$i]}  Stop: ${Stop[$i]} CurrFile: ${Files[$i]} "
	AdjustmentStart=1
	AdjustmentStop=3
	TempStart=`expr "${Start[$i]}" + "$AdjustmentStart" `
	TempStop=`expr "${Stop[$i]}" - "$AdjustmentStop" `
	Expr=" -n -e '$TempStart,$TempStop p' ${Files[$i]} >> $OutputFileName "
	eval sed "$Expr" 
	echo "Exprn : $Expr"
	#exit
done


