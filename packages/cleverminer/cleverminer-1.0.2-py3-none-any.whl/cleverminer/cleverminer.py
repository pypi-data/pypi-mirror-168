import sys #line:18
import time #line:19
import copy #line:20
from time import strftime #line:22
from time import gmtime #line:23
import pandas as pd #line:25
import numpy #line:26
class cleverminer :#line:28
    version_string ="1.0.2"#line:30
    def __init__ (O0OO0OOO0OO0O0O0O ,**O000OOOOO00O000O0 ):#line:32
        O0OO0OOO0OO0O0O0O ._print_disclaimer ()#line:33
        O0OO0OOO0OO0O0O0O .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:42
        O0OO0OOO0OO0O0O0O .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True }#line:46
        O0OO0OOO0OO0O0O0O .kwargs =None #line:47
        if len (O000OOOOO00O000O0 )>0 :#line:48
            O0OO0OOO0OO0O0O0O .kwargs =O000OOOOO00O000O0 #line:49
        O0OO0OOO0OO0O0O0O .verbosity ={}#line:50
        O0OO0OOO0OO0O0O0O .verbosity ['debug']=False #line:51
        O0OO0OOO0OO0O0O0O .verbosity ['print_rules']=False #line:52
        O0OO0OOO0OO0O0O0O .verbosity ['print_hashes']=True #line:53
        O0OO0OOO0OO0O0O0O .verbosity ['last_hash_time']=0 #line:54
        O0OO0OOO0OO0O0O0O .verbosity ['hint']=False #line:55
        if "opts"in O000OOOOO00O000O0 :#line:56
            O0OO0OOO0OO0O0O0O ._set_opts (O000OOOOO00O000O0 .get ("opts"))#line:57
        if "opts"in O000OOOOO00O000O0 :#line:58
            if "verbose"in O000OOOOO00O000O0 .get ('opts'):#line:59
                if O000OOOOO00O000O0 ['verbose'].upper ()=='FULL':#line:60
                    O0OO0OOO0OO0O0O0O .verbosity ['debug']=True #line:61
                    O0OO0OOO0OO0O0O0O .verbosity ['print_rules']=True #line:62
                    O0OO0OOO0OO0O0O0O .verbosity ['print_hashes']=False #line:63
                    O0OO0OOO0OO0O0O0O .verbosity ['hint']=True #line:64
                elif O000OOOOO00O000O0 ['verbose'].upper ()=='RULES':#line:65
                    O0OO0OOO0OO0O0O0O .verbosity ['debug']=False #line:66
                    O0OO0OOO0OO0O0O0O .verbosity ['print_rules']=True #line:67
                    O0OO0OOO0OO0O0O0O .verbosity ['print_hashes']=True #line:68
                    O0OO0OOO0OO0O0O0O .verbosity ['hint']=True #line:69
                elif O000OOOOO00O000O0 ['verbose'].upper ()=='HINT':#line:70
                    O0OO0OOO0OO0O0O0O .verbosity ['debug']=False #line:71
                    O0OO0OOO0OO0O0O0O .verbosity ['print_rules']=False #line:72
                    O0OO0OOO0OO0O0O0O .verbosity ['print_hashes']=True #line:73
                    O0OO0OOO0OO0O0O0O .verbosity ['last_hash_time']=0 #line:74
                    O0OO0OOO0OO0O0O0O .verbosity ['hint']=True #line:75
        O0OO0OOO0OO0O0O0O ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:76
        if not (O0OO0OOO0OO0O0O0O ._is_py310 ):#line:77
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:78
        else :#line:79
            if (O0OO0OOO0OO0O0O0O .verbosity ['debug']):#line:80
                print ("Python 3.10+ detected.")#line:81
        O0OO0OOO0OO0O0O0O ._initialized =False #line:82
        O0OO0OOO0OO0O0O0O ._init_data ()#line:83
        O0OO0OOO0OO0O0O0O ._init_task ()#line:84
        if len (O000OOOOO00O000O0 )>0 :#line:85
            if "df"in O000OOOOO00O000O0 :#line:86
                O0OO0OOO0OO0O0O0O ._prep_data (O000OOOOO00O000O0 .get ("df"))#line:87
            else :#line:88
                print ("Missing dataframe. Cannot initialize.")#line:89
                O0OO0OOO0OO0O0O0O ._initialized =False #line:90
                return #line:91
            OO00OOO000O0O00O0 =O000OOOOO00O000O0 .get ("proc",None )#line:92
            if not (OO00OOO000O0O00O0 ==None ):#line:93
                O0OO0OOO0OO0O0O0O ._calculate (**O000OOOOO00O000O0 )#line:94
            else :#line:96
                if O0OO0OOO0OO0O0O0O .verbosity ['debug']:#line:97
                    print ("INFO: just initialized")#line:98
        O0OO0OOO0OO0O0O0O ._initialized =True #line:99
    def _set_opts (O00OOO0O0O00O0000 ,O00OOO0OOOOO000O0 ):#line:101
        if "no_optimizations"in O00OOO0OOOOO000O0 :#line:102
            O00OOO0O0O00O0000 .options ['optimizations']=not (O00OOO0OOOOO000O0 ['no_optimizations'])#line:103
            print ("No optimization will be made.")#line:104
        if "max_rules"in O00OOO0OOOOO000O0 :#line:105
            O00OOO0O0O00O0000 .options ['max_rules']=O00OOO0OOOOO000O0 ['max_rules']#line:106
        if "max_categories"in O00OOO0OOOOO000O0 :#line:107
            O00OOO0O0O00O0000 .options ['max_categories']=O00OOO0OOOOO000O0 ['max_categories']#line:108
            if O00OOO0O0O00O0000 .verbosity ['debug']==True :#line:109
                print (f"Maximum number of categories set to {O00OOO0O0O00O0000.options['max_categories']}")#line:110
    def _init_data (O00OOOO000O0O0000 ):#line:113
        O00OOOO000O0O0000 .data ={}#line:115
        O00OOOO000O0O0000 .data ["varname"]=[]#line:116
        O00OOOO000O0O0000 .data ["catnames"]=[]#line:117
        O00OOOO000O0O0000 .data ["vtypes"]=[]#line:118
        O00OOOO000O0O0000 .data ["dm"]=[]#line:119
        O00OOOO000O0O0000 .data ["rows_count"]=int (0 )#line:120
        O00OOOO000O0O0000 .data ["data_prepared"]=0 #line:121
    def _init_task (O000OO00O00O0O0O0 ):#line:123
        if "opts"in O000OO00O00O0O0O0 .kwargs :#line:125
            O000OO00O00O0O0O0 ._set_opts (O000OO00O00O0O0O0 .kwargs .get ("opts"))#line:126
        O000OO00O00O0O0O0 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:136
        O000OO00O00O0O0O0 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:140
        O000OO00O00O0O0O0 .rulelist =[]#line:141
        O000OO00O00O0O0O0 .stats ['total_cnt']=0 #line:143
        O000OO00O00O0O0O0 .stats ['total_valid']=0 #line:144
        O000OO00O00O0O0O0 .stats ['control_number']=0 #line:145
        O000OO00O00O0O0O0 .result ={}#line:146
        O000OO00O00O0O0O0 ._opt_base =None #line:147
        O000OO00O00O0O0O0 ._opt_relbase =None #line:148
        O000OO00O00O0O0O0 ._opt_base1 =None #line:149
        O000OO00O00O0O0O0 ._opt_relbase1 =None #line:150
        O000OO00O00O0O0O0 ._opt_base2 =None #line:151
        O000OO00O00O0O0O0 ._opt_relbase2 =None #line:152
        OOO000O000O00O0O0 =None #line:153
        if not (O000OO00O00O0O0O0 .kwargs ==None ):#line:154
            OOO000O000O00O0O0 =O000OO00O00O0O0O0 .kwargs .get ("quantifiers",None )#line:155
            if not (OOO000O000O00O0O0 ==None ):#line:156
                for OO00O00OO0OO0OOO0 in OOO000O000O00O0O0 .keys ():#line:157
                    if OO00O00OO0OO0OOO0 .upper ()=='BASE':#line:158
                        O000OO00O00O0O0O0 ._opt_base =OOO000O000O00O0O0 .get (OO00O00OO0OO0OOO0 )#line:159
                    if OO00O00OO0OO0OOO0 .upper ()=='RELBASE':#line:160
                        O000OO00O00O0O0O0 ._opt_relbase =OOO000O000O00O0O0 .get (OO00O00OO0OO0OOO0 )#line:161
                    if (OO00O00OO0OO0OOO0 .upper ()=='FRSTBASE')|(OO00O00OO0OO0OOO0 .upper ()=='BASE1'):#line:162
                        O000OO00O00O0O0O0 ._opt_base1 =OOO000O000O00O0O0 .get (OO00O00OO0OO0OOO0 )#line:163
                    if (OO00O00OO0OO0OOO0 .upper ()=='SCNDBASE')|(OO00O00OO0OO0OOO0 .upper ()=='BASE2'):#line:164
                        O000OO00O00O0O0O0 ._opt_base2 =OOO000O000O00O0O0 .get (OO00O00OO0OO0OOO0 )#line:165
                    if (OO00O00OO0OO0OOO0 .upper ()=='FRSTRELBASE')|(OO00O00OO0OO0OOO0 .upper ()=='RELBASE1'):#line:166
                        O000OO00O00O0O0O0 ._opt_relbase1 =OOO000O000O00O0O0 .get (OO00O00OO0OO0OOO0 )#line:167
                    if (OO00O00OO0OO0OOO0 .upper ()=='SCNDRELBASE')|(OO00O00OO0OO0OOO0 .upper ()=='RELBASE2'):#line:168
                        O000OO00O00O0O0O0 ._opt_relbase2 =OOO000O000O00O0O0 .get (OO00O00OO0OO0OOO0 )#line:169
            else :#line:170
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:171
        else :#line:172
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:173
    def mine (OOOO0O000000O0O0O ,**O00O00OOOOO0O0000 ):#line:176
        if not (OOOO0O000000O0O0O ._initialized ):#line:177
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:178
            return #line:179
        OOOO0O000000O0O0O .kwargs =None #line:180
        if len (O00O00OOOOO0O0000 )>0 :#line:181
            OOOO0O000000O0O0O .kwargs =O00O00OOOOO0O0000 #line:182
        OOOO0O000000O0O0O ._init_task ()#line:183
        if len (O00O00OOOOO0O0000 )>0 :#line:184
            OOO0OO000OO000OO0 =O00O00OOOOO0O0000 .get ("proc",None )#line:185
            if not (OOO0OO000OO000OO0 ==None ):#line:186
                OOOO0O000000O0O0O ._calc_all (**O00O00OOOOO0O0000 )#line:187
            else :#line:188
                print ("Rule mining procedure missing")#line:189
    def _get_ver (O000OOO00O0O0OO0O ):#line:192
        return O000OOO00O0O0OO0O .version_string #line:193
    def _print_disclaimer (OO00OO0O000OO00O0 ):#line:195
        print (f"Cleverminer version {OO00OO0O000OO00O0._get_ver()}. Note: This version is for personal and educational use only. If you need PRO version (support, fixing structures for compactibility in future versions for production deployment, additional development, licensing of commercial use of subroutines used), feel free to ask authors. Most of these functionalities are maintained in best-effort, as soon as this project is at given conditions for free use and rapid development is needed, they cannot be guaranteed.")#line:197
    def _prep_data (O0OOOOO0OO00000O0 ,OOOOO00OO0O000O0O ):#line:203
        print ("Starting data preparation ...")#line:204
        O0OOOOO0OO00000O0 ._init_data ()#line:205
        O0OOOOO0OO00000O0 .stats ['start_prep_time']=time .time ()#line:206
        O0OOOOO0OO00000O0 .data ["rows_count"]=OOOOO00OO0O000O0O .shape [0 ]#line:207
        for O000OOO0000OOOO0O in OOOOO00OO0O000O0O .select_dtypes (exclude =['category']).columns :#line:208
            OOOOO00OO0O000O0O [O000OOO0000OOOO0O ]=OOOOO00OO0O000O0O [O000OOO0000OOOO0O ].apply (str )#line:209
        try :#line:210
            O000000O000OOO000 =pd .DataFrame .from_records ([(OOOO00OOO0OOOOO00 ,OOOOO00OO0O000O0O [OOOO00OOO0OOOOO00 ].nunique ())for OOOO00OOO0OOOOO00 in OOOOO00OO0O000O0O .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:212
        except :#line:213
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:214
            O0O00OO00OO00000O =""#line:215
            try :#line:216
                for O000OOO0000OOOO0O in OOOOO00OO0O000O0O .columns :#line:217
                    O0O00OO00OO00000O =O000OOO0000OOOO0O #line:218
                    print (f"...column {O000OOO0000OOOO0O} has {int(OOOOO00OO0O000O0O[O000OOO0000OOOO0O].nunique())} values")#line:219
            except :#line:220
                print (f"... detected : column {O0O00OO00OO00000O} has unsupported type: {type(OOOOO00OO0O000O0O[O000OOO0000OOOO0O])}.")#line:221
                exit (1 )#line:222
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:223
            exit (1 )#line:224
        if O0OOOOO0OO00000O0 .verbosity ['hint']:#line:227
            print ("Quick profile of input data: unique value counts are:")#line:228
            print (O000000O000OOO000 )#line:229
            for O000OOO0000OOOO0O in OOOOO00OO0O000O0O .columns :#line:230
                if OOOOO00OO0O000O0O [O000OOO0000OOOO0O ].nunique ()<O0OOOOO0OO00000O0 .options ['max_categories']:#line:231
                    OOOOO00OO0O000O0O [O000OOO0000OOOO0O ]=OOOOO00OO0O000O0O [O000OOO0000OOOO0O ].astype ('category')#line:232
                else :#line:233
                    print (f"WARNING: attribute {O000OOO0000OOOO0O} has more than {O0OOOOO0OO00000O0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:234
                    del OOOOO00OO0O000O0O [O000OOO0000OOOO0O ]#line:235
        print ("Encoding columns into bit-form...")#line:236
        O0OO0O0OOO0O0O0O0 =0 #line:237
        O0OO0O0O0000OOO0O =0 #line:238
        for O00OOOOOOO0OOO0O0 in OOOOO00OO0O000O0O :#line:239
            if O0OOOOO0OO00000O0 .verbosity ['debug']:#line:241
                print ('Column: '+O00OOOOOOO0OOO0O0 )#line:242
            O0OOOOO0OO00000O0 .data ["varname"].append (O00OOOOOOO0OOO0O0 )#line:243
            O0O0O0O00OO0OOO00 =pd .get_dummies (OOOOO00OO0O000O0O [O00OOOOOOO0OOO0O0 ])#line:244
            O0OO00O000O000O0O =0 #line:245
            if (OOOOO00OO0O000O0O .dtypes [O00OOOOOOO0OOO0O0 ].name =='category'):#line:246
                O0OO00O000O000O0O =1 #line:247
            O0OOOOO0OO00000O0 .data ["vtypes"].append (O0OO00O000O000O0O )#line:248
            OOO0OOO00OO00OOOO =0 #line:251
            OO00OOOO00O0O00OO =[]#line:252
            O0O00O0OO0O0OO000 =[]#line:253
            for OOOOOO00OO0OOO00O in O0O0O0O00OO0OOO00 :#line:255
                if O0OOOOO0OO00000O0 .verbosity ['debug']:#line:257
                    print ('....category : '+str (OOOOOO00OO0OOO00O )+" @ "+str (time .time ()))#line:258
                OO00OOOO00O0O00OO .append (OOOOOO00OO0OOO00O )#line:259
                O0OO0000O00O0OO0O =int (0 )#line:260
                O0OOOOO0000O00000 =O0O0O0O00OO0OOO00 [OOOOOO00OO0OOO00O ].values #line:261
                O0OOO000OOOOO0O00 =numpy .packbits (O0OOOOO0000O00000 ,bitorder ='little')#line:263
                O0OO0000O00O0OO0O =int .from_bytes (O0OOO000OOOOO0O00 ,byteorder ='little')#line:264
                O0O00O0OO0O0OO000 .append (O0OO0000O00O0OO0O )#line:265
                OOO0OOO00OO00OOOO +=1 #line:283
                O0OO0O0O0000OOO0O +=1 #line:284
            O0OOOOO0OO00000O0 .data ["catnames"].append (OO00OOOO00O0O00OO )#line:286
            O0OOOOO0OO00000O0 .data ["dm"].append (O0O00O0OO0O0OO000 )#line:287
        print ("Encoding columns into bit-form...done")#line:289
        if O0OOOOO0OO00000O0 .verbosity ['hint']:#line:290
            print (f"List of attributes for analysis is: {O0OOOOO0OO00000O0.data['varname']}")#line:291
            print (f"List of category names for individual attributes is : {O0OOOOO0OO00000O0.data['catnames']}")#line:292
        if O0OOOOO0OO00000O0 .verbosity ['debug']:#line:293
            print (f"List of vtypes is (all should be 1) : {O0OOOOO0OO00000O0.data['vtypes']}")#line:294
        O0OOOOO0OO00000O0 .data ["data_prepared"]=1 #line:296
        print ("Data preparation finished.")#line:297
        if O0OOOOO0OO00000O0 .verbosity ['debug']:#line:298
            print ('Number of variables : '+str (len (O0OOOOO0OO00000O0 .data ["dm"])))#line:299
            print ('Total number of categories in all variables : '+str (O0OO0O0O0000OOO0O ))#line:300
        O0OOOOO0OO00000O0 .stats ['end_prep_time']=time .time ()#line:301
        if O0OOOOO0OO00000O0 .verbosity ['debug']:#line:302
            print ('Time needed for data preparation : ',str (O0OOOOO0OO00000O0 .stats ['end_prep_time']-O0OOOOO0OO00000O0 .stats ['start_prep_time']))#line:303
    def _bitcount (O000OO0O0000O0OO0 ,OOO000OO000OOO000 ):#line:305
        OO0O0OO0O0O0O0000 =None #line:306
        if (O000OO0O0000O0OO0 ._is_py310 ):#line:307
            OO0O0OO0O0O0O0000 =OOO000OO000OOO000 .bit_count ()#line:308
        else :#line:309
            OO0O0OO0O0O0O0000 =bin (OOO000OO000OOO000 ).count ("1")#line:310
        return OO0O0OO0O0O0O0000 #line:311
    def _verifyCF (OO00O0000OOOOOO0O ,_OO00000OOOO00000O ):#line:314
        OO00OO000000OOO00 =OO00O0000OOOOOO0O ._bitcount (_OO00000OOOO00000O )#line:315
        O00O000OOO0OO0O0O =[]#line:316
        O000O0000OOO0O0OO =[]#line:317
        OOOOO0O0O00000000 =0 #line:318
        O0OOO00O00O0OOOO0 =0 #line:319
        OO00000OO0000OO0O =0 #line:320
        OOOO0OOOOO0OOOO00 =0 #line:321
        O0OOOO00O0O000OOO =0 #line:322
        OO0OOOOOOO0000O0O =0 #line:323
        O0O0OO00O000OOO00 =0 #line:324
        OOOOOOOOOOOOO0O00 =0 #line:325
        O00O0OOO00000O0OO =0 #line:326
        OO0OO0OO00OOOOO00 =OO00O0000OOOOOO0O .data ["dm"][OO00O0000OOOOOO0O .data ["varname"].index (OO00O0000OOOOOO0O .kwargs .get ('target'))]#line:327
        for OOO00O0OOOOOOO00O in range (len (OO0OO0OO00OOOOO00 )):#line:328
            O0OOO00O00O0OOOO0 =OOOOO0O0O00000000 #line:329
            OOOOO0O0O00000000 =OO00O0000OOOOOO0O ._bitcount (_OO00000OOOO00000O &OO0OO0OO00OOOOO00 [OOO00O0OOOOOOO00O ])#line:330
            O00O000OOO0OO0O0O .append (OOOOO0O0O00000000 )#line:331
            if OOO00O0OOOOOOO00O >0 :#line:332
                if (OOOOO0O0O00000000 >O0OOO00O00O0OOOO0 ):#line:333
                    if (OO00000OO0000OO0O ==1 ):#line:334
                        OOOOOOOOOOOOO0O00 +=1 #line:335
                    else :#line:336
                        OOOOOOOOOOOOO0O00 =1 #line:337
                    if OOOOOOOOOOOOO0O00 >OOOO0OOOOO0OOOO00 :#line:338
                        OOOO0OOOOO0OOOO00 =OOOOOOOOOOOOO0O00 #line:339
                    OO00000OO0000OO0O =1 #line:340
                    OO0OOOOOOO0000O0O +=1 #line:341
                if (OOOOO0O0O00000000 <O0OOO00O00O0OOOO0 ):#line:342
                    if (OO00000OO0000OO0O ==-1 ):#line:343
                        O00O0OOO00000O0OO +=1 #line:344
                    else :#line:345
                        O00O0OOO00000O0OO =1 #line:346
                    if O00O0OOO00000O0OO >O0OOOO00O0O000OOO :#line:347
                        O0OOOO00O0O000OOO =O00O0OOO00000O0OO #line:348
                    OO00000OO0000OO0O =-1 #line:349
                    O0O0OO00O000OOO00 +=1 #line:350
                if (OOOOO0O0O00000000 ==O0OOO00O00O0OOOO0 ):#line:351
                    OO00000OO0000OO0O =0 #line:352
                    O00O0OOO00000O0OO =0 #line:353
                    OOOOOOOOOOOOO0O00 =0 #line:354
        O0OO0OOO00OO00O0O =True #line:357
        for O0OOO0OO00OOOOO00 in OO00O0000OOOOOO0O .quantifiers .keys ():#line:358
            if O0OOO0OO00OOOOO00 .upper ()=='BASE':#line:359
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=OO00OO000000OOO00 )#line:360
            if O0OOO0OO00OOOOO00 .upper ()=='RELBASE':#line:361
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=OO00OO000000OOO00 *1.0 /OO00O0000OOOOOO0O .data ["rows_count"])#line:362
            if O0OOO0OO00OOOOO00 .upper ()=='S_UP':#line:363
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=OOOO0OOOOO0OOOO00 )#line:364
            if O0OOO0OO00OOOOO00 .upper ()=='S_DOWN':#line:365
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=O0OOOO00O0O000OOO )#line:366
            if O0OOO0OO00OOOOO00 .upper ()=='S_ANY_UP':#line:367
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=OOOO0OOOOO0OOOO00 )#line:368
            if O0OOO0OO00OOOOO00 .upper ()=='S_ANY_DOWN':#line:369
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=O0OOOO00O0O000OOO )#line:370
            if O0OOO0OO00OOOOO00 .upper ()=='MAX':#line:371
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=max (O00O000OOO0OO0O0O ))#line:372
            if O0OOO0OO00OOOOO00 .upper ()=='MIN':#line:373
                O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=min (O00O000OOO0OO0O0O ))#line:374
            if O0OOO0OO00OOOOO00 .upper ()=='RELMAX':#line:375
                if sum (O00O000OOO0OO0O0O )>0 :#line:376
                    O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=max (O00O000OOO0OO0O0O )*1.0 /sum (O00O000OOO0OO0O0O ))#line:377
                else :#line:378
                    O0OO0OOO00OO00O0O =False #line:379
            if O0OOO0OO00OOOOO00 .upper ()=='RELMAX_LEQ':#line:380
                if sum (O00O000OOO0OO0O0O )>0 :#line:381
                    O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )>=max (O00O000OOO0OO0O0O )*1.0 /sum (O00O000OOO0OO0O0O ))#line:382
                else :#line:383
                    O0OO0OOO00OO00O0O =False #line:384
            if O0OOO0OO00OOOOO00 .upper ()=='RELMIN':#line:385
                if sum (O00O000OOO0OO0O0O )>0 :#line:386
                    O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )<=min (O00O000OOO0OO0O0O )*1.0 /sum (O00O000OOO0OO0O0O ))#line:387
                else :#line:388
                    O0OO0OOO00OO00O0O =False #line:389
            if O0OOO0OO00OOOOO00 .upper ()=='RELMIN_LEQ':#line:390
                if sum (O00O000OOO0OO0O0O )>0 :#line:391
                    O0OO0OOO00OO00O0O =O0OO0OOO00OO00O0O and (OO00O0000OOOOOO0O .quantifiers .get (O0OOO0OO00OOOOO00 )>=min (O00O000OOO0OO0O0O )*1.0 /sum (O00O000OOO0OO0O0O ))#line:392
                else :#line:393
                    O0OO0OOO00OO00O0O =False #line:394
        OOO0O0O00O00OO000 ={}#line:395
        if O0OO0OOO00OO00O0O ==True :#line:396
            OO00O0000OOOOOO0O .stats ['total_valid']+=1 #line:398
            OOO0O0O00O00OO000 ["base"]=OO00OO000000OOO00 #line:399
            OOO0O0O00O00OO000 ["rel_base"]=OO00OO000000OOO00 *1.0 /OO00O0000OOOOOO0O .data ["rows_count"]#line:400
            OOO0O0O00O00OO000 ["s_up"]=OOOO0OOOOO0OOOO00 #line:401
            OOO0O0O00O00OO000 ["s_down"]=O0OOOO00O0O000OOO #line:402
            OOO0O0O00O00OO000 ["s_any_up"]=OO0OOOOOOO0000O0O #line:403
            OOO0O0O00O00OO000 ["s_any_down"]=O0O0OO00O000OOO00 #line:404
            OOO0O0O00O00OO000 ["max"]=max (O00O000OOO0OO0O0O )#line:405
            OOO0O0O00O00OO000 ["min"]=min (O00O000OOO0OO0O0O )#line:406
            if sum (O00O000OOO0OO0O0O )>0 :#line:409
                OOO0O0O00O00OO000 ["rel_max"]=max (O00O000OOO0OO0O0O )*1.0 /sum (O00O000OOO0OO0O0O )#line:410
                OOO0O0O00O00OO000 ["rel_min"]=min (O00O000OOO0OO0O0O )*1.0 /sum (O00O000OOO0OO0O0O )#line:411
            else :#line:412
                OOO0O0O00O00OO000 ["rel_max"]=0 #line:413
                OOO0O0O00O00OO000 ["rel_min"]=0 #line:414
            OOO0O0O00O00OO000 ["hist"]=O00O000OOO0OO0O0O #line:415
        return O0OO0OOO00OO00O0O ,OOO0O0O00O00OO000 #line:417
    def _verify4ft (O0OO00000O000O00O ,_O0O00O00O0000OOOO ):#line:419
        O0O0O0000OO0O000O ={}#line:420
        OOOOO0000O00O0OOO =0 #line:421
        for O000OO000O00OOOO0 in O0OO00000O000O00O .task_actinfo ['cedents']:#line:422
            O0O0O0000OO0O000O [O000OO000O00OOOO0 ['cedent_type']]=O000OO000O00OOOO0 ['filter_value']#line:424
            OOOOO0000O00O0OOO =OOOOO0000O00O0OOO +1 #line:425
        OO00O0O0OOO00O0OO =O0OO00000O000O00O ._bitcount (O0O0O0000OO0O000O ['ante']&O0O0O0000OO0O000O ['succ']&O0O0O0000OO0O000O ['cond'])#line:427
        OOO0000O0OO000O0O =None #line:428
        OOO0000O0OO000O0O =0 #line:429
        if OO00O0O0OOO00O0OO >0 :#line:438
            OOO0000O0OO000O0O =O0OO00000O000O00O ._bitcount (O0O0O0000OO0O000O ['ante']&O0O0O0000OO0O000O ['succ']&O0O0O0000OO0O000O ['cond'])*1.0 /O0OO00000O000O00O ._bitcount (O0O0O0000OO0O000O ['ante']&O0O0O0000OO0O000O ['cond'])#line:439
        O000OO0O0O00OO0OO =1 <<O0OO00000O000O00O .data ["rows_count"]#line:441
        OOOOO0000OOO0OOOO =O0OO00000O000O00O ._bitcount (O0O0O0000OO0O000O ['ante']&O0O0O0000OO0O000O ['succ']&O0O0O0000OO0O000O ['cond'])#line:442
        OO0O000OO00O000OO =O0OO00000O000O00O ._bitcount (O0O0O0000OO0O000O ['ante']&~(O000OO0O0O00OO0OO |O0O0O0000OO0O000O ['succ'])&O0O0O0000OO0O000O ['cond'])#line:443
        O000OO000O00OOOO0 =O0OO00000O000O00O ._bitcount (~(O000OO0O0O00OO0OO |O0O0O0000OO0O000O ['ante'])&O0O0O0000OO0O000O ['succ']&O0O0O0000OO0O000O ['cond'])#line:444
        OOOOO0O000OOO0O0O =O0OO00000O000O00O ._bitcount (~(O000OO0O0O00OO0OO |O0O0O0000OO0O000O ['ante'])&~(O000OO0O0O00OO0OO |O0O0O0000OO0O000O ['succ'])&O0O0O0000OO0O000O ['cond'])#line:445
        OOO00OO0O00O0O000 =0 #line:446
        if (OOOOO0000OOO0OOOO +OO0O000OO00O000OO )*(OOOOO0000OOO0OOOO +O000OO000O00OOOO0 )>0 :#line:447
            OOO00OO0O00O0O000 =OOOOO0000OOO0OOOO *(OOOOO0000OOO0OOOO +OO0O000OO00O000OO +O000OO000O00OOOO0 +OOOOO0O000OOO0O0O )/(OOOOO0000OOO0OOOO +OO0O000OO00O000OO )/(OOOOO0000OOO0OOOO +O000OO000O00OOOO0 )-1 #line:448
        else :#line:449
            OOO00OO0O00O0O000 =None #line:450
        O0OO0OO0O00O0O000 =0 #line:451
        if (OOOOO0000OOO0OOOO +OO0O000OO00O000OO )*(OOOOO0000OOO0OOOO +O000OO000O00OOOO0 )>0 :#line:452
            O0OO0OO0O00O0O000 =1 -OOOOO0000OOO0OOOO *(OOOOO0000OOO0OOOO +OO0O000OO00O000OO +O000OO000O00OOOO0 +OOOOO0O000OOO0O0O )/(OOOOO0000OOO0OOOO +OO0O000OO00O000OO )/(OOOOO0000OOO0OOOO +O000OO000O00OOOO0 )#line:453
        else :#line:454
            O0OO0OO0O00O0O000 =None #line:455
        O000O000OO0O0000O =True #line:456
        for OO0000O0OO0O0OOO0 in O0OO00000O000O00O .quantifiers .keys ():#line:457
            if OO0000O0OO0O0OOO0 .upper ()=='BASE':#line:458
                O000O000OO0O0000O =O000O000OO0O0000O and (O0OO00000O000O00O .quantifiers .get (OO0000O0OO0O0OOO0 )<=OO00O0O0OOO00O0OO )#line:459
            if OO0000O0OO0O0OOO0 .upper ()=='RELBASE':#line:460
                O000O000OO0O0000O =O000O000OO0O0000O and (O0OO00000O000O00O .quantifiers .get (OO0000O0OO0O0OOO0 )<=OO00O0O0OOO00O0OO *1.0 /O0OO00000O000O00O .data ["rows_count"])#line:461
            if (OO0000O0OO0O0OOO0 .upper ()=='PIM')or (OO0000O0OO0O0OOO0 .upper ()=='CONF'):#line:462
                O000O000OO0O0000O =O000O000OO0O0000O and (O0OO00000O000O00O .quantifiers .get (OO0000O0OO0O0OOO0 )<=OOO0000O0OO000O0O )#line:463
            if OO0000O0OO0O0OOO0 .upper ()=='AAD':#line:464
                if OOO00OO0O00O0O000 !=None :#line:465
                    O000O000OO0O0000O =O000O000OO0O0000O and (O0OO00000O000O00O .quantifiers .get (OO0000O0OO0O0OOO0 )<=OOO00OO0O00O0O000 )#line:466
                else :#line:467
                    O000O000OO0O0000O =False #line:468
            if OO0000O0OO0O0OOO0 .upper ()=='BAD':#line:469
                if O0OO0OO0O00O0O000 !=None :#line:470
                    O000O000OO0O0000O =O000O000OO0O0000O and (O0OO00000O000O00O .quantifiers .get (OO0000O0OO0O0OOO0 )<=O0OO0OO0O00O0O000 )#line:471
                else :#line:472
                    O000O000OO0O0000O =False #line:473
            OOOOOOOOO0O000OOO ={}#line:474
        if O000O000OO0O0000O ==True :#line:475
            O0OO00000O000O00O .stats ['total_valid']+=1 #line:477
            OOOOOOOOO0O000OOO ["base"]=OO00O0O0OOO00O0OO #line:478
            OOOOOOOOO0O000OOO ["rel_base"]=OO00O0O0OOO00O0OO *1.0 /O0OO00000O000O00O .data ["rows_count"]#line:479
            OOOOOOOOO0O000OOO ["conf"]=OOO0000O0OO000O0O #line:480
            OOOOOOOOO0O000OOO ["aad"]=OOO00OO0O00O0O000 #line:481
            OOOOOOOOO0O000OOO ["bad"]=O0OO0OO0O00O0O000 #line:482
            OOOOOOOOO0O000OOO ["fourfold"]=[OOOOO0000OOO0OOOO ,OO0O000OO00O000OO ,O000OO000O00OOOO0 ,OOOOO0O000OOO0O0O ]#line:483
        return O000O000OO0O0000O ,OOOOOOOOO0O000OOO #line:487
    def _verifysd4ft (OOOO000OO00O0O000 ,_OOOO0OOOOOOOOO000 ):#line:489
        OOOO000O0OOOOOOO0 ={}#line:490
        O0000000O00OOO0OO =0 #line:491
        for O0000O0O0OO00OOO0 in OOOO000OO00O0O000 .task_actinfo ['cedents']:#line:492
            OOOO000O0OOOOOOO0 [O0000O0O0OO00OOO0 ['cedent_type']]=O0000O0O0OO00OOO0 ['filter_value']#line:494
            O0000000O00OOO0OO =O0000000O00OOO0OO +1 #line:495
        O000OOOOOOO00O0OO =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])#line:497
        O00O000OOOOO00000 =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])#line:498
        O000O0O0O00000O00 =None #line:499
        OO0O0000000OOOO0O =0 #line:500
        OO0O00OO0000O000O =0 #line:501
        if O000OOOOOOO00O0OO >0 :#line:510
            OO0O0000000OOOO0O =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])*1.0 /OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])#line:511
        if O00O000OOOOO00000 >0 :#line:512
            OO0O00OO0000O000O =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])*1.0 /OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])#line:513
        O0OO0O0O0OO0O0OO0 =1 <<OOOO000OO00O0O000 .data ["rows_count"]#line:515
        O0000000O000OO000 =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])#line:516
        OO0O0O00OOOOOOOOO =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['succ'])&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])#line:517
        O0O0000000OOO00O0 =OOOO000OO00O0O000 ._bitcount (~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['ante'])&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])#line:518
        O0OOOOOOOOOOOO00O =OOOO000OO00O0O000 ._bitcount (~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['ante'])&~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['succ'])&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['frst'])#line:519
        O000O0000O0O00O00 =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])#line:520
        OOOO000O0O0OO00O0 =OOOO000OO00O0O000 ._bitcount (OOOO000O0OOOOOOO0 ['ante']&~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['succ'])&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])#line:521
        O0OO0O0O0OO000O0O =OOOO000OO00O0O000 ._bitcount (~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['ante'])&OOOO000O0OOOOOOO0 ['succ']&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])#line:522
        OO00O0O0OOO0OO000 =OOOO000OO00O0O000 ._bitcount (~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['ante'])&~(O0OO0O0O0OO0O0OO0 |OOOO000O0OOOOOOO0 ['succ'])&OOOO000O0OOOOOOO0 ['cond']&OOOO000O0OOOOOOO0 ['scnd'])#line:523
        OOOO00O0OO000O0O0 =True #line:524
        for OO00O00OO000OO000 in OOOO000OO00O0O000 .quantifiers .keys ():#line:525
            if (OO00O00OO000OO000 .upper ()=='FRSTBASE')|(OO00O00OO000OO000 .upper ()=='BASE1'):#line:526
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=O000OOOOOOO00O0OO )#line:527
            if (OO00O00OO000OO000 .upper ()=='SCNDBASE')|(OO00O00OO000OO000 .upper ()=='BASE2'):#line:528
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=O00O000OOOOO00000 )#line:529
            if (OO00O00OO000OO000 .upper ()=='FRSTRELBASE')|(OO00O00OO000OO000 .upper ()=='RELBASE1'):#line:530
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=O000OOOOOOO00O0OO *1.0 /OOOO000OO00O0O000 .data ["rows_count"])#line:531
            if (OO00O00OO000OO000 .upper ()=='SCNDRELBASE')|(OO00O00OO000OO000 .upper ()=='RELBASE2'):#line:532
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=O00O000OOOOO00000 *1.0 /OOOO000OO00O0O000 .data ["rows_count"])#line:533
            if (OO00O00OO000OO000 .upper ()=='FRSTPIM')|(OO00O00OO000OO000 .upper ()=='PIM1')|(OO00O00OO000OO000 .upper ()=='FRSTCONF')|(OO00O00OO000OO000 .upper ()=='CONF1'):#line:534
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=OO0O0000000OOOO0O )#line:535
            if (OO00O00OO000OO000 .upper ()=='SCNDPIM')|(OO00O00OO000OO000 .upper ()=='PIM2')|(OO00O00OO000OO000 .upper ()=='SCNDCONF')|(OO00O00OO000OO000 .upper ()=='CONF2'):#line:536
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=OO0O00OO0000O000O )#line:537
            if (OO00O00OO000OO000 .upper ()=='DELTAPIM')|(OO00O00OO000OO000 .upper ()=='DELTACONF'):#line:538
                OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=OO0O0000000OOOO0O -OO0O00OO0000O000O )#line:539
            if (OO00O00OO000OO000 .upper ()=='RATIOPIM')|(OO00O00OO000OO000 .upper ()=='RATIOCONF'):#line:542
                if (OO0O00OO0000O000O >0 ):#line:543
                    OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )<=OO0O0000000OOOO0O *1.0 /OO0O00OO0000O000O )#line:544
                else :#line:545
                    OOOO00O0OO000O0O0 =False #line:546
            if (OO00O00OO000OO000 .upper ()=='RATIOPIM_LEQ')|(OO00O00OO000OO000 .upper ()=='RATIOCONF_LEQ'):#line:547
                if (OO0O00OO0000O000O >0 ):#line:548
                    OOOO00O0OO000O0O0 =OOOO00O0OO000O0O0 and (OOOO000OO00O0O000 .quantifiers .get (OO00O00OO000OO000 )>=OO0O0000000OOOO0O *1.0 /OO0O00OO0000O000O )#line:549
                else :#line:550
                    OOOO00O0OO000O0O0 =False #line:551
        OOO00OOOOO00OO0OO ={}#line:552
        if OOOO00O0OO000O0O0 ==True :#line:553
            OOOO000OO00O0O000 .stats ['total_valid']+=1 #line:555
            OOO00OOOOO00OO0OO ["base1"]=O000OOOOOOO00O0OO #line:556
            OOO00OOOOO00OO0OO ["base2"]=O00O000OOOOO00000 #line:557
            OOO00OOOOO00OO0OO ["rel_base1"]=O000OOOOOOO00O0OO *1.0 /OOOO000OO00O0O000 .data ["rows_count"]#line:558
            OOO00OOOOO00OO0OO ["rel_base2"]=O00O000OOOOO00000 *1.0 /OOOO000OO00O0O000 .data ["rows_count"]#line:559
            OOO00OOOOO00OO0OO ["conf1"]=OO0O0000000OOOO0O #line:560
            OOO00OOOOO00OO0OO ["conf2"]=OO0O00OO0000O000O #line:561
            OOO00OOOOO00OO0OO ["deltaconf"]=OO0O0000000OOOO0O -OO0O00OO0000O000O #line:562
            if (OO0O00OO0000O000O >0 ):#line:563
                OOO00OOOOO00OO0OO ["ratioconf"]=OO0O0000000OOOO0O *1.0 /OO0O00OO0000O000O #line:564
            else :#line:565
                OOO00OOOOO00OO0OO ["ratioconf"]=None #line:566
            OOO00OOOOO00OO0OO ["fourfold1"]=[O0000000O000OO000 ,OO0O0O00OOOOOOOOO ,O0O0000000OOO00O0 ,O0OOOOOOOOOOOO00O ]#line:567
            OOO00OOOOO00OO0OO ["fourfold2"]=[O000O0000O0O00O00 ,OOOO000O0O0OO00O0 ,O0OO0O0O0OO000O0O ,OO00O0O0OOO0OO000 ]#line:568
        return OOOO00O0OO000O0O0 ,OOO00OOOOO00OO0OO #line:572
    def _verifynewact4ft (OO0OO0OO0O0O0OOOO ,_OOOOOO0O0O0O0O0OO ):#line:574
        O000OO00O00O00O00 ={}#line:575
        for OO000OOO0000000OO in OO0OO0OO0O0O0OOOO .task_actinfo ['cedents']:#line:576
            O000OO00O00O00O00 [OO000OOO0000000OO ['cedent_type']]=OO000OOO0000000OO ['filter_value']#line:578
        O0O0OOOO00O000O00 =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond'])#line:580
        O0O0OO0O00OOOO00O =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond']&O000OO00O00O00O00 ['antv']&O000OO00O00O00O00 ['sucv'])#line:581
        OOO0OOO000OOOOOO0 =None #line:582
        O0O00OO0O0OOOO000 =0 #line:583
        OO00O0O0OO000O0OO =0 #line:584
        if O0O0OOOO00O000O00 >0 :#line:593
            O0O00OO0O0OOOO000 =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond'])*1.0 /OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['cond'])#line:594
        if O0O0OO0O00OOOO00O >0 :#line:595
            OO00O0O0OO000O0OO =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond']&O000OO00O00O00O00 ['antv']&O000OO00O00O00O00 ['sucv'])*1.0 /OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['cond']&O000OO00O00O00O00 ['antv'])#line:597
        OOO00OOOO00OO0OO0 =1 <<OO0OO0OO0O0O0OOOO .rows_count #line:599
        OO00O00OOO00000OO =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond'])#line:600
        O00O000O0O00OOOO0 =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&~(OOO00OOOO00OO0OO0 |O000OO00O00O00O00 ['succ'])&O000OO00O00O00O00 ['cond'])#line:601
        O00OOOOO0O0O00O0O =OO0OO0OO0O0O0OOOO ._bitcount (~(OOO00OOOO00OO0OO0 |O000OO00O00O00O00 ['ante'])&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond'])#line:602
        OO000OOO00O0OOO00 =OO0OO0OO0O0O0OOOO ._bitcount (~(OOO00OOOO00OO0OO0 |O000OO00O00O00O00 ['ante'])&~(OOO00OOOO00OO0OO0 |O000OO00O00O00O00 ['succ'])&O000OO00O00O00O00 ['cond'])#line:603
        OOOO000OO0000OO0O =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond']&O000OO00O00O00O00 ['antv']&O000OO00O00O00O00 ['sucv'])#line:604
        O000OO00OOO000O0O =OO0OO0OO0O0O0OOOO ._bitcount (O000OO00O00O00O00 ['ante']&~(OOO00OOOO00OO0OO0 |(O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['sucv']))&O000OO00O00O00O00 ['cond'])#line:605
        OOO00O0O0O0OOO00O =OO0OO0OO0O0O0OOOO ._bitcount (~(OOO00OOOO00OO0OO0 |(O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['antv']))&O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['cond']&O000OO00O00O00O00 ['sucv'])#line:606
        OO000OOOOOOO0O0OO =OO0OO0OO0O0O0OOOO ._bitcount (~(OOO00OOOO00OO0OO0 |(O000OO00O00O00O00 ['ante']&O000OO00O00O00O00 ['antv']))&~(OOO00OOOO00OO0OO0 |(O000OO00O00O00O00 ['succ']&O000OO00O00O00O00 ['sucv']))&O000OO00O00O00O00 ['cond'])#line:607
        O0O0OO0OO00OO0OO0 =True #line:608
        for O0OOOO0000OOOO00O in OO0OO0OO0O0O0OOOO .quantifiers .keys ():#line:609
            if (O0OOOO0000OOOO00O =='PreBase')|(O0OOOO0000OOOO00O =='Base1'):#line:610
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O0OOOO00O000O00 )#line:611
            if (O0OOOO0000OOOO00O =='PostBase')|(O0OOOO0000OOOO00O =='Base2'):#line:612
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O0OO0O00OOOO00O )#line:613
            if (O0OOOO0000OOOO00O =='PreRelBase')|(O0OOOO0000OOOO00O =='RelBase1'):#line:614
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O0OOOO00O000O00 *1.0 /OO0OO0OO0O0O0OOOO .data ["rows_count"])#line:615
            if (O0OOOO0000OOOO00O =='PostRelBase')|(O0OOOO0000OOOO00O =='RelBase2'):#line:616
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O0OO0O00OOOO00O *1.0 /OO0OO0OO0O0O0OOOO .data ["rows_count"])#line:617
            if (O0OOOO0000OOOO00O =='Prepim')|(O0OOOO0000OOOO00O =='pim1')|(O0OOOO0000OOOO00O =='PreConf')|(O0OOOO0000OOOO00O =='conf1'):#line:618
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O00OO0O0OOOO000 )#line:619
            if (O0OOOO0000OOOO00O =='Postpim')|(O0OOOO0000OOOO00O =='pim2')|(O0OOOO0000OOOO00O =='PostConf')|(O0OOOO0000OOOO00O =='conf2'):#line:620
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=OO00O0O0OO000O0OO )#line:621
            if (O0OOOO0000OOOO00O =='Deltapim')|(O0OOOO0000OOOO00O =='DeltaConf'):#line:622
                O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O00OO0O0OOOO000 -OO00O0O0OO000O0OO )#line:623
            if (O0OOOO0000OOOO00O =='Ratiopim')|(O0OOOO0000OOOO00O =='RatioConf'):#line:626
                if (OO00O0O0OO000O0OO >0 ):#line:627
                    O0O0OO0OO00OO0OO0 =O0O0OO0OO00OO0OO0 and (OO0OO0OO0O0O0OOOO .quantifiers .get (O0OOOO0000OOOO00O )<=O0O00OO0O0OOOO000 *1.0 /OO00O0O0OO000O0OO )#line:628
                else :#line:629
                    O0O0OO0OO00OO0OO0 =False #line:630
        OOO00OO0O00OOOO00 ={}#line:631
        if O0O0OO0OO00OO0OO0 ==True :#line:632
            OO0OO0OO0O0O0OOOO .stats ['total_valid']+=1 #line:634
            OOO00OO0O00OOOO00 ["base1"]=O0O0OOOO00O000O00 #line:635
            OOO00OO0O00OOOO00 ["base2"]=O0O0OO0O00OOOO00O #line:636
            OOO00OO0O00OOOO00 ["rel_base1"]=O0O0OOOO00O000O00 *1.0 /OO0OO0OO0O0O0OOOO .data ["rows_count"]#line:637
            OOO00OO0O00OOOO00 ["rel_base2"]=O0O0OO0O00OOOO00O *1.0 /OO0OO0OO0O0O0OOOO .data ["rows_count"]#line:638
            OOO00OO0O00OOOO00 ["conf1"]=O0O00OO0O0OOOO000 #line:639
            OOO00OO0O00OOOO00 ["conf2"]=OO00O0O0OO000O0OO #line:640
            OOO00OO0O00OOOO00 ["deltaconf"]=O0O00OO0O0OOOO000 -OO00O0O0OO000O0OO #line:641
            if (OO00O0O0OO000O0OO >0 ):#line:642
                OOO00OO0O00OOOO00 ["ratioconf"]=O0O00OO0O0OOOO000 *1.0 /OO00O0O0OO000O0OO #line:643
            else :#line:644
                OOO00OO0O00OOOO00 ["ratioconf"]=None #line:645
            OOO00OO0O00OOOO00 ["fourfoldpre"]=[OO00O00OOO00000OO ,O00O000O0O00OOOO0 ,O00OOOOO0O0O00O0O ,OO000OOO00O0OOO00 ]#line:646
            OOO00OO0O00OOOO00 ["fourfoldpost"]=[OOOO000OO0000OO0O ,O000OO00OOO000O0O ,OOO00O0O0O0OOO00O ,OO000OOOOOOO0O0OO ]#line:647
        return O0O0OO0OO00OO0OO0 ,OOO00OO0O00OOOO00 #line:649
    def _verifyact4ft (OO000OO0OO00OOO00 ,_O0OO0OO0000OO0O00 ):#line:651
        O0O0000O0OO0OOO00 ={}#line:652
        for O0O00O0OO0O0OOOOO in OO000OO0OO00OOO00 .task_actinfo ['cedents']:#line:653
            O0O0000O0OO0OOO00 [O0O00O0OO0O0OOOOO ['cedent_type']]=O0O00O0OO0O0OOOOO ['filter_value']#line:655
        O0OOO000O0O0O0OOO =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv-']&O0O0000O0OO0OOO00 ['sucv-'])#line:657
        OO00OO00O000OO0O0 =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv+']&O0O0000O0OO0OOO00 ['sucv+'])#line:658
        O00OOOOO0000O0000 =None #line:659
        OOO00OOO0O000O00O =0 #line:660
        OOOO0O0OO000OOO00 =0 #line:661
        if O0OOO000O0O0O0OOO >0 :#line:670
            OOO00OOO0O000O00O =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv-']&O0O0000O0OO0OOO00 ['sucv-'])*1.0 /OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv-'])#line:672
        if OO00OO00O000OO0O0 >0 :#line:673
            OOOO0O0OO000OOO00 =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv+']&O0O0000O0OO0OOO00 ['sucv+'])*1.0 /OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv+'])#line:675
        O0OO0000OO0OOOOOO =1 <<OO000OO0OO00OOO00 .data ["rows_count"]#line:677
        O0OO00OO00O0OOOO0 =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv-']&O0O0000O0OO0OOO00 ['sucv-'])#line:678
        O0O0000O0OO00O0OO =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['antv-']&~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['sucv-']))&O0O0000O0OO0OOO00 ['cond'])#line:679
        OOO0O00O0O0O0O0O0 =OO000OO0OO00OOO00 ._bitcount (~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['antv-']))&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['sucv-'])#line:680
        O0000OO0O00O000OO =OO000OO0OO00OOO00 ._bitcount (~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['antv-']))&~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['sucv-']))&O0O0000O0OO0OOO00 ['cond'])#line:681
        O0OO0OOO000O0OOO0 =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['antv+']&O0O0000O0OO0OOO00 ['sucv+'])#line:682
        OOO00O00000OOO0OO =OO000OO0OO00OOO00 ._bitcount (O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['antv+']&~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['sucv+']))&O0O0000O0OO0OOO00 ['cond'])#line:683
        OOOO0OOO00OO00O0O =OO000OO0OO00OOO00 ._bitcount (~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['antv+']))&O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['cond']&O0O0000O0OO0OOO00 ['sucv+'])#line:684
        OO0OO0000OO0OO0OO =OO000OO0OO00OOO00 ._bitcount (~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['ante']&O0O0000O0OO0OOO00 ['antv+']))&~(O0OO0000OO0OOOOOO |(O0O0000O0OO0OOO00 ['succ']&O0O0000O0OO0OOO00 ['sucv+']))&O0O0000O0OO0OOO00 ['cond'])#line:685
        OOO0O000000O0000O =True #line:686
        for O0O00OOOO00OO0O0O in OO000OO0OO00OOO00 .quantifiers .keys ():#line:687
            if (O0O00OOOO00OO0O0O =='PreBase')|(O0O00OOOO00OO0O0O =='Base1'):#line:688
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=O0OOO000O0O0O0OOO )#line:689
            if (O0O00OOOO00OO0O0O =='PostBase')|(O0O00OOOO00OO0O0O =='Base2'):#line:690
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=OO00OO00O000OO0O0 )#line:691
            if (O0O00OOOO00OO0O0O =='PreRelBase')|(O0O00OOOO00OO0O0O =='RelBase1'):#line:692
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=O0OOO000O0O0O0OOO *1.0 /OO000OO0OO00OOO00 .data ["rows_count"])#line:693
            if (O0O00OOOO00OO0O0O =='PostRelBase')|(O0O00OOOO00OO0O0O =='RelBase2'):#line:694
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=OO00OO00O000OO0O0 *1.0 /OO000OO0OO00OOO00 .data ["rows_count"])#line:695
            if (O0O00OOOO00OO0O0O =='Prepim')|(O0O00OOOO00OO0O0O =='pim1')|(O0O00OOOO00OO0O0O =='PreConf')|(O0O00OOOO00OO0O0O =='conf1'):#line:696
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=OOO00OOO0O000O00O )#line:697
            if (O0O00OOOO00OO0O0O =='Postpim')|(O0O00OOOO00OO0O0O =='pim2')|(O0O00OOOO00OO0O0O =='PostConf')|(O0O00OOOO00OO0O0O =='conf2'):#line:698
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=OOOO0O0OO000OOO00 )#line:699
            if (O0O00OOOO00OO0O0O =='Deltapim')|(O0O00OOOO00OO0O0O =='DeltaConf'):#line:700
                OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=OOO00OOO0O000O00O -OOOO0O0OO000OOO00 )#line:701
            if (O0O00OOOO00OO0O0O =='Ratiopim')|(O0O00OOOO00OO0O0O =='RatioConf'):#line:704
                if (OOO00OOO0O000O00O >0 ):#line:705
                    OOO0O000000O0000O =OOO0O000000O0000O and (OO000OO0OO00OOO00 .quantifiers .get (O0O00OOOO00OO0O0O )<=OOOO0O0OO000OOO00 *1.0 /OOO00OOO0O000O00O )#line:706
                else :#line:707
                    OOO0O000000O0000O =False #line:708
        O0O00OO00O00OO0OO ={}#line:709
        if OOO0O000000O0000O ==True :#line:710
            OO000OO0OO00OOO00 .stats ['total_valid']+=1 #line:712
            O0O00OO00O00OO0OO ["base1"]=O0OOO000O0O0O0OOO #line:713
            O0O00OO00O00OO0OO ["base2"]=OO00OO00O000OO0O0 #line:714
            O0O00OO00O00OO0OO ["rel_base1"]=O0OOO000O0O0O0OOO *1.0 /OO000OO0OO00OOO00 .data ["rows_count"]#line:715
            O0O00OO00O00OO0OO ["rel_base2"]=OO00OO00O000OO0O0 *1.0 /OO000OO0OO00OOO00 .data ["rows_count"]#line:716
            O0O00OO00O00OO0OO ["conf1"]=OOO00OOO0O000O00O #line:717
            O0O00OO00O00OO0OO ["conf2"]=OOOO0O0OO000OOO00 #line:718
            O0O00OO00O00OO0OO ["deltaconf"]=OOO00OOO0O000O00O -OOOO0O0OO000OOO00 #line:719
            if (OOO00OOO0O000O00O >0 ):#line:720
                O0O00OO00O00OO0OO ["ratioconf"]=OOOO0O0OO000OOO00 *1.0 /OOO00OOO0O000O00O #line:721
            else :#line:722
                O0O00OO00O00OO0OO ["ratioconf"]=None #line:723
            O0O00OO00O00OO0OO ["fourfoldpre"]=[O0OO00OO00O0OOOO0 ,O0O0000O0OO00O0OO ,OOO0O00O0O0O0O0O0 ,O0000OO0O00O000OO ]#line:724
            O0O00OO00O00OO0OO ["fourfoldpost"]=[O0OO0OOO000O0OOO0 ,OOO00O00000OOO0OO ,OOOO0OOO00OO00O0O ,OO0OO0000OO0OO0OO ]#line:725
        return OOO0O000000O0000O ,O0O00OO00O00OO0OO #line:727
    def _verify_opt (O0O0O0OOOO0000OOO ,OO00O0OOO0O00OO00 ,OO00OOO00O0O0O000 ):#line:729
        O0O0O0OOOO0000OOO .stats ['total_ver']+=1 #line:730
        O0OOOO00O00OOO00O =False #line:731
        if not (OO00O0OOO0O00OO00 ['optim'].get ('only_con')):#line:734
            return False #line:735
        if not (O0O0O0OOOO0000OOO .options ['optimizations']):#line:738
            return False #line:740
        OOO0O0OOO0OO00OOO ={}#line:742
        for OO0O0OOOO0000O000 in O0O0O0OOOO0000OOO .task_actinfo ['cedents']:#line:743
            OOO0O0OOO0OO00OOO [OO0O0OOOO0000O000 ['cedent_type']]=OO0O0OOOO0000O000 ['filter_value']#line:745
        O0O0OO0OO000OO0O0 =1 <<O0O0O0OOOO0000OOO .data ["rows_count"]#line:747
        OO00000000O0O000O =O0O0OO0OO000OO0O0 -1 #line:748
        OOOO0000O000O0O0O =""#line:749
        OO00000O00O0OOOOO =0 #line:750
        if (OOO0O0OOO0OO00OOO .get ('ante')!=None ):#line:751
            OO00000000O0O000O =OO00000000O0O000O &OOO0O0OOO0OO00OOO ['ante']#line:752
        if (OOO0O0OOO0OO00OOO .get ('succ')!=None ):#line:753
            OO00000000O0O000O =OO00000000O0O000O &OOO0O0OOO0OO00OOO ['succ']#line:754
        if (OOO0O0OOO0OO00OOO .get ('cond')!=None ):#line:755
            OO00000000O0O000O =OO00000000O0O000O &OOO0O0OOO0OO00OOO ['cond']#line:756
        O0O000OOO00000O00 =None #line:759
        if (O0O0O0OOOO0000OOO .proc =='CFMiner')|(O0O0O0OOOO0000OOO .proc =='4ftMiner'):#line:784
            OO0O0000OOO0OO00O =O0O0O0OOOO0000OOO ._bitcount (OO00000000O0O000O )#line:785
            if not (O0O0O0OOOO0000OOO ._opt_base ==None ):#line:786
                if not (O0O0O0OOOO0000OOO ._opt_base <=OO0O0000OOO0OO00O ):#line:787
                    O0OOOO00O00OOO00O =True #line:788
            if not (O0O0O0OOOO0000OOO ._opt_relbase ==None ):#line:790
                if not (O0O0O0OOOO0000OOO ._opt_relbase <=OO0O0000OOO0OO00O *1.0 /O0O0O0OOOO0000OOO .data ["rows_count"]):#line:791
                    O0OOOO00O00OOO00O =True #line:792
        if (O0O0O0OOOO0000OOO .proc =='SD4ftMiner'):#line:794
            OO0O0000OOO0OO00O =O0O0O0OOOO0000OOO ._bitcount (OO00000000O0O000O )#line:795
            if (not (O0O0O0OOOO0000OOO ._opt_base1 ==None ))&(not (O0O0O0OOOO0000OOO ._opt_base2 ==None )):#line:796
                if not (max (O0O0O0OOOO0000OOO ._opt_base1 ,O0O0O0OOOO0000OOO ._opt_base2 )<=OO0O0000OOO0OO00O ):#line:797
                    O0OOOO00O00OOO00O =True #line:799
            if (not (O0O0O0OOOO0000OOO ._opt_relbase1 ==None ))&(not (O0O0O0OOOO0000OOO ._opt_relbase2 ==None )):#line:800
                if not (max (O0O0O0OOOO0000OOO ._opt_relbase1 ,O0O0O0OOOO0000OOO ._opt_relbase2 )<=OO0O0000OOO0OO00O *1.0 /O0O0O0OOOO0000OOO .data ["rows_count"]):#line:801
                    O0OOOO00O00OOO00O =True #line:802
        return O0OOOO00O00OOO00O #line:804
        if O0O0O0OOOO0000OOO .proc =='CFMiner':#line:807
            if (OO00OOO00O0O0O000 ['cedent_type']=='cond')&(OO00OOO00O0O0O000 ['defi'].get ('type')=='con'):#line:808
                OO0O0000OOO0OO00O =bin (OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:809
                OOOO000000OOOOOOO =True #line:810
                for OOO00O0O0O000OOO0 in O0O0O0OOOO0000OOO .quantifiers .keys ():#line:811
                    if OOO00O0O0O000OOO0 =='Base':#line:812
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=OO0O0000OOO0OO00O )#line:813
                        if not (OOOO000000OOOOOOO ):#line:814
                            print (f"...optimization : base is {OO0O0000OOO0OO00O} for {OO00OOO00O0O0O000['generated_string']}")#line:815
                    if OOO00O0O0O000OOO0 =='RelBase':#line:816
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=OO0O0000OOO0OO00O *1.0 /O0O0O0OOOO0000OOO .data ["rows_count"])#line:817
                        if not (OOOO000000OOOOOOO ):#line:818
                            print (f"...optimization : base is {OO0O0000OOO0OO00O} for {OO00OOO00O0O0O000['generated_string']}")#line:819
                O0OOOO00O00OOO00O =not (OOOO000000OOOOOOO )#line:820
        elif O0O0O0OOOO0000OOO .proc =='4ftMiner':#line:821
            if (OO00OOO00O0O0O000 ['cedent_type']=='cond')&(OO00OOO00O0O0O000 ['defi'].get ('type')=='con'):#line:822
                OO0O0000OOO0OO00O =bin (OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:823
                OOOO000000OOOOOOO =True #line:824
                for OOO00O0O0O000OOO0 in O0O0O0OOOO0000OOO .quantifiers .keys ():#line:825
                    if OOO00O0O0O000OOO0 =='Base':#line:826
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=OO0O0000OOO0OO00O )#line:827
                        if not (OOOO000000OOOOOOO ):#line:828
                            print (f"...optimization : base is {OO0O0000OOO0OO00O} for {OO00OOO00O0O0O000['generated_string']}")#line:829
                    if OOO00O0O0O000OOO0 =='RelBase':#line:830
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=OO0O0000OOO0OO00O *1.0 /O0O0O0OOOO0000OOO .data ["rows_count"])#line:831
                        if not (OOOO000000OOOOOOO ):#line:832
                            print (f"...optimization : base is {OO0O0000OOO0OO00O} for {OO00OOO00O0O0O000['generated_string']}")#line:833
                O0OOOO00O00OOO00O =not (OOOO000000OOOOOOO )#line:834
            if (OO00OOO00O0O0O000 ['cedent_type']=='ante')&(OO00OOO00O0O0O000 ['defi'].get ('type')=='con'):#line:835
                OO0O0000OOO0OO00O =bin (OOO0O0OOO0OO00OOO ['ante']&OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:836
                OOOO000000OOOOOOO =True #line:837
                for OOO00O0O0O000OOO0 in O0O0O0OOOO0000OOO .quantifiers .keys ():#line:838
                    if OOO00O0O0O000OOO0 =='Base':#line:839
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=OO0O0000OOO0OO00O )#line:840
                        if not (OOOO000000OOOOOOO ):#line:841
                            print (f"...optimization : ANTE: base is {OO0O0000OOO0OO00O} for {OO00OOO00O0O0O000['generated_string']}")#line:842
                    if OOO00O0O0O000OOO0 =='RelBase':#line:843
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=OO0O0000OOO0OO00O *1.0 /O0O0O0OOOO0000OOO .data ["rows_count"])#line:844
                        if not (OOOO000000OOOOOOO ):#line:845
                            print (f"...optimization : ANTE:  base is {OO0O0000OOO0OO00O} for {OO00OOO00O0O0O000['generated_string']}")#line:846
                O0OOOO00O00OOO00O =not (OOOO000000OOOOOOO )#line:847
            if (OO00OOO00O0O0O000 ['cedent_type']=='succ')&(OO00OOO00O0O0O000 ['defi'].get ('type')=='con'):#line:848
                OO0O0000OOO0OO00O =bin (OOO0O0OOO0OO00OOO ['ante']&OOO0O0OOO0OO00OOO ['cond']&OOO0O0OOO0OO00OOO ['succ']).count ("1")#line:849
                O0O000OOO00000O00 =0 #line:850
                if OO0O0000OOO0OO00O >0 :#line:851
                    O0O000OOO00000O00 =bin (OOO0O0OOO0OO00OOO ['ante']&OOO0O0OOO0OO00OOO ['succ']&OOO0O0OOO0OO00OOO ['cond']).count ("1")*1.0 /bin (OOO0O0OOO0OO00OOO ['ante']&OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:852
                O0O0OO0OO000OO0O0 =1 <<O0O0O0OOOO0000OOO .data ["rows_count"]#line:853
                O000O0O00O0O0OO0O =bin (OOO0O0OOO0OO00OOO ['ante']&OOO0O0OOO0OO00OOO ['succ']&OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:854
                O0OOO0O0OO000O0O0 =bin (OOO0O0OOO0OO00OOO ['ante']&~(O0O0OO0OO000OO0O0 |OOO0O0OOO0OO00OOO ['succ'])&OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:855
                OO0O0OOOO0000O000 =bin (~(O0O0OO0OO000OO0O0 |OOO0O0OOO0OO00OOO ['ante'])&OOO0O0OOO0OO00OOO ['succ']&OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:856
                O0OO00000O0OO0OOO =bin (~(O0O0OO0OO000OO0O0 |OOO0O0OOO0OO00OOO ['ante'])&~(O0O0OO0OO000OO0O0 |OOO0O0OOO0OO00OOO ['succ'])&OOO0O0OOO0OO00OOO ['cond']).count ("1")#line:857
                OOOO000000OOOOOOO =True #line:858
                for OOO00O0O0O000OOO0 in O0O0O0OOOO0000OOO .quantifiers .keys ():#line:859
                    if OOO00O0O0O000OOO0 =='pim':#line:860
                        OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=O0O000OOO00000O00 )#line:861
                    if not (OOOO000000OOOOOOO ):#line:862
                        print (f"...optimization : SUCC:  pim is {O0O000OOO00000O00} for {OO00OOO00O0O0O000['generated_string']}")#line:863
                    if OOO00O0O0O000OOO0 =='aad':#line:865
                        if (O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 )*(O000O0O00O0O0OO0O +OO0O0OOOO0000O000 )>0 :#line:866
                            OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=O000O0O00O0O0OO0O *(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 +OO0O0OOOO0000O000 +O0OO00000O0OO0OOO )/(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 )/(O000O0O00O0O0OO0O +OO0O0OOOO0000O000 )-1 )#line:867
                        else :#line:868
                            OOOO000000OOOOOOO =False #line:869
                        if not (OOOO000000OOOOOOO ):#line:870
                            O000O0OO00O0OO000 =O000O0O00O0O0OO0O *(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 +OO0O0OOOO0000O000 +O0OO00000O0OO0OOO )/(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 )/(O000O0O00O0O0OO0O +OO0O0OOOO0000O000 )-1 #line:871
                            print (f"...optimization : SUCC:  aad is {O000O0OO00O0OO000} for {OO00OOO00O0O0O000['generated_string']}")#line:872
                    if OOO00O0O0O000OOO0 =='bad':#line:873
                        if (O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 )*(O000O0O00O0O0OO0O +OO0O0OOOO0000O000 )>0 :#line:874
                            OOOO000000OOOOOOO =OOOO000000OOOOOOO and (O0O0O0OOOO0000OOO .quantifiers .get (OOO00O0O0O000OOO0 )<=1 -O000O0O00O0O0OO0O *(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 +OO0O0OOOO0000O000 +O0OO00000O0OO0OOO )/(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 )/(O000O0O00O0O0OO0O +OO0O0OOOO0000O000 ))#line:875
                        else :#line:876
                            OOOO000000OOOOOOO =False #line:877
                        if not (OOOO000000OOOOOOO ):#line:878
                            O00000OO0O0000OOO =1 -O000O0O00O0O0OO0O *(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 +OO0O0OOOO0000O000 +O0OO00000O0OO0OOO )/(O000O0O00O0O0OO0O +O0OOO0O0OO000O0O0 )/(O000O0O00O0O0OO0O +OO0O0OOOO0000O000 )#line:879
                            print (f"...optimization : SUCC:  bad is {O00000OO0O0000OOO} for {OO00OOO00O0O0O000['generated_string']}")#line:880
                O0OOOO00O00OOO00O =not (OOOO000000OOOOOOO )#line:881
        if (O0OOOO00O00OOO00O ):#line:882
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {OO00OOO00O0O0O000['cedent_type']}")#line:883
        return O0OOOO00O00OOO00O #line:884
    def _print (O00O0OOO0O0OOO0OO ,OOOOOOOOO0O0O00O0 ,_OO0OO0O0000O0O0O0 ,_OOOOO0O00OO00O000 ):#line:887
        if (len (_OO0OO0O0000O0O0O0 ))!=len (_OOOOO0O00OO00O000 ):#line:888
            print ("DIFF IN LEN for following cedent : "+str (len (_OO0OO0O0000O0O0O0 ))+" vs "+str (len (_OOOOO0O00OO00O000 )))#line:889
            print ("trace cedent : "+str (_OO0OO0O0000O0O0O0 )+", traces "+str (_OOOOO0O00OO00O000 ))#line:890
        OOO0000O0O00OO0O0 =''#line:891
        OOO00O0OO000OOO0O ={}#line:892
        OOOOOO000000O0OOO =[]#line:893
        for O0O0000O00O0O0OOO in range (len (_OO0OO0O0000O0O0O0 )):#line:894
            OOOO0000O00O0000O =O00O0OOO0O0OOO0OO .data ["varname"].index (OOOOOOOOO0O0O00O0 ['defi'].get ('attributes')[_OO0OO0O0000O0O0O0 [O0O0000O00O0O0OOO ]].get ('name'))#line:895
            OOO0000O0O00OO0O0 =OOO0000O0O00OO0O0 +O00O0OOO0O0OOO0OO .data ["varname"][OOOO0000O00O0000O ]+'('#line:897
            OOOOOO000000O0OOO .append (OOOO0000O00O0000O )#line:898
            O00O0O0O0OO000OO0 =[]#line:899
            for OOOOO0OO0O00O000O in _OOOOO0O00OO00O000 [O0O0000O00O0O0OOO ]:#line:900
                OOO0000O0O00OO0O0 =OOO0000O0O00OO0O0 +str (O00O0OOO0O0OOO0OO .data ["catnames"][OOOO0000O00O0000O ][OOOOO0OO0O00O000O ])+" "#line:901
                O00O0O0O0OO000OO0 .append (str (O00O0OOO0O0OOO0OO .data ["catnames"][OOOO0000O00O0000O ][OOOOO0OO0O00O000O ]))#line:902
            OOO0000O0O00OO0O0 =OOO0000O0O00OO0O0 [:-1 ]+')'#line:903
            OOO00O0OO000OOO0O [O00O0OOO0O0OOO0OO .data ["varname"][OOOO0000O00O0000O ]]=O00O0O0O0OO000OO0 #line:904
            if O0O0000O00O0O0OOO +1 <len (_OO0OO0O0000O0O0O0 ):#line:905
                OOO0000O0O00OO0O0 =OOO0000O0O00OO0O0 +' & '#line:906
        return OOO0000O0O00OO0O0 ,OOO00O0OO000OOO0O ,OOOOOO000000O0OOO #line:910
    def _print_hypo (O00O00O000O000000 ,OO0OOO0OO000O0000 ):#line:912
        O00O00O000O000000 .print_rule (OO0OOO0OO000O0000 )#line:913
    def _print_rule (OO0OO00000OO0O0O0 ,O0OO0O00000O000OO ):#line:915
        if OO0OO00000OO0O0O0 .verbosity ['print_rules']:#line:916
            print ('Rules info : '+str (O0OO0O00000O000OO ['params']))#line:917
            for OO00O000O0OOO0OOO in OO0OO00000OO0O0O0 .task_actinfo ['cedents']:#line:918
                print (OO00O000O0OOO0OOO ['cedent_type']+' = '+OO00O000O0OOO0OOO ['generated_string'])#line:919
    def _genvar (OOO00OOO0OOOOOO00 ,O00O0OO00O00OOOO0 ,O0O00OOOO000OO000 ,_OO000O00O0O0O00OO ,_OOOO000O00OO0OO0O ,_OOOOOOOOO00O0OO0O ,_OOOOOOO00OO0OOO00 ,_O0O0O00OO0OOOO0O0 ):#line:921
        for O0000000O00O0O0O0 in range (O0O00OOOO000OO000 ['num_cedent']):#line:922
            if len (_OO000O00O0O0O00OO )==0 or O0000000O00O0O0O0 >_OO000O00O0O0O00OO [-1 ]:#line:923
                _OO000O00O0O0O00OO .append (O0000000O00O0O0O0 )#line:924
                O0OO0OOOO000O000O =OOO00OOO0OOOOOO00 .data ["varname"].index (O0O00OOOO000OO000 ['defi'].get ('attributes')[O0000000O00O0O0O0 ].get ('name'))#line:925
                _O0O0O0OO00O00000O =O0O00OOOO000OO000 ['defi'].get ('attributes')[O0000000O00O0O0O0 ].get ('minlen')#line:926
                _OO0O0O0OOO00OO0OO =O0O00OOOO000OO000 ['defi'].get ('attributes')[O0000000O00O0O0O0 ].get ('maxlen')#line:927
                _OO0000O0OO000OO0O =O0O00OOOO000OO000 ['defi'].get ('attributes')[O0000000O00O0O0O0 ].get ('type')#line:928
                OOOOO0O0O0000OOO0 =len (OOO00OOO0OOOOOO00 .data ["dm"][O0OO0OOOO000O000O ])#line:929
                _O0000O00O0OOO0O00 =[]#line:930
                _OOOO000O00OO0OO0O .append (_O0000O00O0OOO0O00 )#line:931
                _OO0OO0OOO0O00OO00 =int (0 )#line:932
                OOO00OOO0OOOOOO00 ._gencomb (O00O0OO00O00OOOO0 ,O0O00OOOO000OO000 ,_OO000O00O0O0O00OO ,_OOOO000O00OO0OO0O ,_O0000O00O0OOO0O00 ,_OOOOOOOOO00O0OO0O ,_OO0OO0OOO0O00OO00 ,OOOOO0O0O0000OOO0 ,_OO0000O0OO000OO0O ,_OOOOOOO00OO0OOO00 ,_O0O0O00OO0OOOO0O0 ,_O0O0O0OO00O00000O ,_OO0O0O0OOO00OO0OO )#line:933
                _OOOO000O00OO0OO0O .pop ()#line:934
                _OO000O00O0O0O00OO .pop ()#line:935
    def _gencomb (O0O0OO0000O000OO0 ,OO0O0O0O0OO00OO0O ,OOO0OOOOO00OO0OO0 ,_OOO000O00O000OOOO ,_OOOO00000O0OOOOOO ,_OOOOOOOOO00OOO00O ,_OO00O0O0O00OO0O0O ,_O00OOOO000OOO00OO ,O000O00OOO0OO0OOO ,_O0OOO0O0OOO00O0O0 ,_OO00O000O0OOO000O ,_OOOOOOO0O00OOOOO0 ,_OO0OO00O0O0O0OOO0 ,_OO0O0000OOO000O0O ):#line:937
        _O0O0OO0OOO0OO00OO =[]#line:938
        if _O0OOO0O0OOO00O0O0 =="subset":#line:939
            if len (_OOOOOOOOO00OOO00O )==0 :#line:940
                _O0O0OO0OOO0OO00OO =range (O000O00OOO0OO0OOO )#line:941
            else :#line:942
                _O0O0OO0OOO0OO00OO =range (_OOOOOOOOO00OOO00O [-1 ]+1 ,O000O00OOO0OO0OOO )#line:943
        elif _O0OOO0O0OOO00O0O0 =="seq":#line:944
            if len (_OOOOOOOOO00OOO00O )==0 :#line:945
                _O0O0OO0OOO0OO00OO =range (O000O00OOO0OO0OOO -_OO0OO00O0O0O0OOO0 +1 )#line:946
            else :#line:947
                if _OOOOOOOOO00OOO00O [-1 ]+1 ==O000O00OOO0OO0OOO :#line:948
                    return #line:949
                O000OOOO0OO0OOO00 =_OOOOOOOOO00OOO00O [-1 ]+1 #line:950
                _O0O0OO0OOO0OO00OO .append (O000OOOO0OO0OOO00 )#line:951
        elif _O0OOO0O0OOO00O0O0 =="lcut":#line:952
            if len (_OOOOOOOOO00OOO00O )==0 :#line:953
                O000OOOO0OO0OOO00 =0 ;#line:954
            else :#line:955
                if _OOOOOOOOO00OOO00O [-1 ]+1 ==O000O00OOO0OO0OOO :#line:956
                    return #line:957
                O000OOOO0OO0OOO00 =_OOOOOOOOO00OOO00O [-1 ]+1 #line:958
            _O0O0OO0OOO0OO00OO .append (O000OOOO0OO0OOO00 )#line:959
        elif _O0OOO0O0OOO00O0O0 =="rcut":#line:960
            if len (_OOOOOOOOO00OOO00O )==0 :#line:961
                O000OOOO0OO0OOO00 =O000O00OOO0OO0OOO -1 ;#line:962
            else :#line:963
                if _OOOOOOOOO00OOO00O [-1 ]==0 :#line:964
                    return #line:965
                O000OOOO0OO0OOO00 =_OOOOOOOOO00OOO00O [-1 ]-1 #line:966
            _O0O0OO0OOO0OO00OO .append (O000OOOO0OO0OOO00 )#line:968
        elif _O0OOO0O0OOO00O0O0 =="one":#line:969
            if len (_OOOOOOOOO00OOO00O )==0 :#line:970
                O00000OOO0O0OOOO0 =O0O0OO0000O000OO0 .data ["varname"].index (OOO0OOOOO00OO0OO0 ['defi'].get ('attributes')[_OOO000O00O000OOOO [-1 ]].get ('name'))#line:971
                try :#line:972
                    O000OOOO0OO0OOO00 =O0O0OO0000O000OO0 .data ["catnames"][O00000OOO0O0OOOO0 ].index (OOO0OOOOO00OO0OO0 ['defi'].get ('attributes')[_OOO000O00O000OOOO [-1 ]].get ('value'))#line:973
                except :#line:974
                    print (f"ERROR: attribute '{OOO0OOOOO00OO0OO0['defi'].get('attributes')[_OOO000O00O000OOOO[-1]].get('name')}' has not value '{OOO0OOOOO00OO0OO0['defi'].get('attributes')[_OOO000O00O000OOOO[-1]].get('value')}'")#line:975
                    exit (1 )#line:976
                _O0O0OO0OOO0OO00OO .append (O000OOOO0OO0OOO00 )#line:977
                _OO0OO00O0O0O0OOO0 =1 #line:978
                _OO0O0000OOO000O0O =1 #line:979
            else :#line:980
                print ("DEBUG: one category should not have more categories")#line:981
                return #line:982
        else :#line:983
            print ("Attribute type "+_O0OOO0O0OOO00O0O0 +" not supported.")#line:984
            return #line:985
        for OOO00OOO0O0O0OOOO in _O0O0OO0OOO0OO00OO :#line:988
                _OOOOOOOOO00OOO00O .append (OOO00OOO0O0O0OOOO )#line:990
                _OOOO00000O0OOOOOO .pop ()#line:991
                _OOOO00000O0OOOOOO .append (_OOOOOOOOO00OOO00O )#line:992
                _OOOOOO0000OOOO0O0 =_O00OOOO000OOO00OO |O0O0OO0000O000OO0 .data ["dm"][O0O0OO0000O000OO0 .data ["varname"].index (OOO0OOOOO00OO0OO0 ['defi'].get ('attributes')[_OOO000O00O000OOOO [-1 ]].get ('name'))][OOO00OOO0O0O0OOOO ]#line:996
                _OO00OOOOOOOOO0O00 =1 #line:998
                if (len (_OOO000O00O000OOOO )<_OO00O000O0OOO000O ):#line:999
                    _OO00OOOOOOOOO0O00 =-1 #line:1000
                if (len (_OOOO00000O0OOOOOO [-1 ])<_OO0OO00O0O0O0OOO0 ):#line:1002
                    _OO00OOOOOOOOO0O00 =0 #line:1003
                _OOOOOOOO0OOO0OOOO =0 #line:1005
                if OOO0OOOOO00OO0OO0 ['defi'].get ('type')=='con':#line:1006
                    _OOOOOOOO0OOO0OOOO =_OO00O0O0O00OO0O0O &_OOOOOO0000OOOO0O0 #line:1007
                else :#line:1008
                    _OOOOOOOO0OOO0OOOO =_OO00O0O0O00OO0O0O |_OOOOOO0000OOOO0O0 #line:1009
                OOO0OOOOO00OO0OO0 ['trace_cedent']=_OOO000O00O000OOOO #line:1010
                OOO0OOOOO00OO0OO0 ['traces']=_OOOO00000O0OOOOOO #line:1011
                OO00OOOO0000000OO ,OO00OO0O000OO0O00 ,OOO000OO00OO00000 =O0O0OO0000O000OO0 ._print (OOO0OOOOO00OO0OO0 ,_OOO000O00O000OOOO ,_OOOO00000O0OOOOOO )#line:1012
                OOO0OOOOO00OO0OO0 ['generated_string']=OO00OOOO0000000OO #line:1013
                OOO0OOOOO00OO0OO0 ['rule']=OO00OO0O000OO0O00 #line:1014
                OOO0OOOOO00OO0OO0 ['filter_value']=_OOOOOOOO0OOO0OOOO #line:1015
                OOO0OOOOO00OO0OO0 ['traces']=copy .deepcopy (_OOOO00000O0OOOOOO )#line:1016
                OOO0OOOOO00OO0OO0 ['trace_cedent']=copy .deepcopy (_OOO000O00O000OOOO )#line:1017
                OOO0OOOOO00OO0OO0 ['trace_cedent_asindata']=copy .deepcopy (OOO000OO00OO00000 )#line:1018
                OO0O0O0O0OO00OO0O ['cedents'].append (OOO0OOOOO00OO0OO0 )#line:1020
                O0O0OOOOOO0O0000O =O0O0OO0000O000OO0 ._verify_opt (OO0O0O0O0OO00OO0O ,OOO0OOOOO00OO0OO0 )#line:1021
                if not (O0O0OOOOOO0O0000O ):#line:1027
                    if _OO00OOOOOOOOO0O00 ==1 :#line:1028
                        if len (OO0O0O0O0OO00OO0O ['cedents_to_do'])==len (OO0O0O0O0OO00OO0O ['cedents']):#line:1030
                            if O0O0OO0000O000OO0 .proc =='CFMiner':#line:1031
                                OO00000O00000O0O0 ,OOOOOO000OOOOO0O0 =O0O0OO0000O000OO0 ._verifyCF (_OOOOOOOO0OOO0OOOO )#line:1032
                            elif O0O0OO0000O000OO0 .proc =='4ftMiner':#line:1033
                                OO00000O00000O0O0 ,OOOOOO000OOOOO0O0 =O0O0OO0000O000OO0 ._verify4ft (_OOOOOO0000OOOO0O0 )#line:1034
                            elif O0O0OO0000O000OO0 .proc =='SD4ftMiner':#line:1035
                                OO00000O00000O0O0 ,OOOOOO000OOOOO0O0 =O0O0OO0000O000OO0 ._verifysd4ft (_OOOOOO0000OOOO0O0 )#line:1036
                            elif O0O0OO0000O000OO0 .proc =='NewAct4ftMiner':#line:1037
                                OO00000O00000O0O0 ,OOOOOO000OOOOO0O0 =O0O0OO0000O000OO0 ._verifynewact4ft (_OOOOOO0000OOOO0O0 )#line:1038
                            elif O0O0OO0000O000OO0 .proc =='Act4ftMiner':#line:1039
                                OO00000O00000O0O0 ,OOOOOO000OOOOO0O0 =O0O0OO0000O000OO0 ._verifyact4ft (_OOOOOO0000OOOO0O0 )#line:1040
                            else :#line:1041
                                print ("Unsupported procedure : "+O0O0OO0000O000OO0 .proc )#line:1042
                                exit (0 )#line:1043
                            if OO00000O00000O0O0 ==True :#line:1044
                                OO000OOOO00OO0000 ={}#line:1045
                                OO000OOOO00OO0000 ["rule_id"]=O0O0OO0000O000OO0 .stats ['total_valid']#line:1046
                                OO000OOOO00OO0000 ["cedents_str"]={}#line:1047
                                OO000OOOO00OO0000 ["cedents_struct"]={}#line:1048
                                OO000OOOO00OO0000 ['traces']={}#line:1049
                                OO000OOOO00OO0000 ['trace_cedent_taskorder']={}#line:1050
                                OO000OOOO00OO0000 ['trace_cedent_dataorder']={}#line:1051
                                for O0OOO0OOOO0000000 in OO0O0O0O0OO00OO0O ['cedents']:#line:1052
                                    OO000OOOO00OO0000 ['cedents_str'][O0OOO0OOOO0000000 ['cedent_type']]=O0OOO0OOOO0000000 ['generated_string']#line:1054
                                    OO000OOOO00OO0000 ['cedents_struct'][O0OOO0OOOO0000000 ['cedent_type']]=O0OOO0OOOO0000000 ['rule']#line:1055
                                    OO000OOOO00OO0000 ['traces'][O0OOO0OOOO0000000 ['cedent_type']]=O0OOO0OOOO0000000 ['traces']#line:1056
                                    OO000OOOO00OO0000 ['trace_cedent_taskorder'][O0OOO0OOOO0000000 ['cedent_type']]=O0OOO0OOOO0000000 ['trace_cedent']#line:1057
                                    OO000OOOO00OO0000 ['trace_cedent_dataorder'][O0OOO0OOOO0000000 ['cedent_type']]=O0OOO0OOOO0000000 ['trace_cedent_asindata']#line:1058
                                OO000OOOO00OO0000 ["params"]=OOOOOO000OOOOO0O0 #line:1060
                                O0O0OO0000O000OO0 ._print_rule (OO000OOOO00OO0000 )#line:1062
                                O0O0OO0000O000OO0 .rulelist .append (OO000OOOO00OO0000 )#line:1068
                            O0O0OO0000O000OO0 .stats ['total_cnt']+=1 #line:1070
                            O0O0OO0000O000OO0 .stats ['total_ver']+=1 #line:1071
                    if _OO00OOOOOOOOO0O00 >=0 :#line:1072
                        if len (OO0O0O0O0OO00OO0O ['cedents_to_do'])>len (OO0O0O0O0OO00OO0O ['cedents']):#line:1073
                            O0O0OO0000O000OO0 ._start_cedent (OO0O0O0O0OO00OO0O )#line:1074
                    OO0O0O0O0OO00OO0O ['cedents'].pop ()#line:1075
                    if (len (_OOO000O00O000OOOO )<_OOOOOOO0O00OOOOO0 ):#line:1076
                        O0O0OO0000O000OO0 ._genvar (OO0O0O0O0OO00OO0O ,OOO0OOOOO00OO0OO0 ,_OOO000O00O000OOOO ,_OOOO00000O0OOOOOO ,_OOOOOOOO0OOO0OOOO ,_OO00O000O0OOO000O ,_OOOOOOO0O00OOOOO0 )#line:1077
                else :#line:1078
                    OO0O0O0O0OO00OO0O ['cedents'].pop ()#line:1079
                if len (_OOOOOOOOO00OOO00O )<_OO0O0000OOO000O0O :#line:1080
                    O0O0OO0000O000OO0 ._gencomb (OO0O0O0O0OO00OO0O ,OOO0OOOOO00OO0OO0 ,_OOO000O00O000OOOO ,_OOOO00000O0OOOOOO ,_OOOOOOOOO00OOO00O ,_OO00O0O0O00OO0O0O ,_OOOOOO0000OOOO0O0 ,O000O00OOO0OO0OOO ,_O0OOO0O0OOO00O0O0 ,_OO00O000O0OOO000O ,_OOOOOOO0O00OOOOO0 ,_OO0OO00O0O0O0OOO0 ,_OO0O0000OOO000O0O )#line:1081
                _OOOOOOOOO00OOO00O .pop ()#line:1082
    def _start_cedent (O00O0O0OO0O0OO0OO ,OOO00OOO0OO0O00OO ):#line:1084
        if len (OOO00OOO0OO0O00OO ['cedents_to_do'])>len (OOO00OOO0OO0O00OO ['cedents']):#line:1085
            _OO000OOOOO0O0O000 =[]#line:1086
            _OOOO00OOO0O0O0O0O =[]#line:1087
            OOOO0O00OOO00OO00 ={}#line:1088
            OOOO0O00OOO00OO00 ['cedent_type']=OOO00OOO0OO0O00OO ['cedents_to_do'][len (OOO00OOO0OO0O00OO ['cedents'])]#line:1089
            OO0OOO0O00O00O0O0 =OOOO0O00OOO00OO00 ['cedent_type']#line:1090
            if ((OO0OOO0O00O00O0O0 [-1 ]=='-')|(OO0OOO0O00O00O0O0 [-1 ]=='+')):#line:1091
                OO0OOO0O00O00O0O0 =OO0OOO0O00O00O0O0 [:-1 ]#line:1092
            OOOO0O00OOO00OO00 ['defi']=O00O0O0OO0O0OO0OO .kwargs .get (OO0OOO0O00O00O0O0 )#line:1094
            if (OOOO0O00OOO00OO00 ['defi']==None ):#line:1095
                print ("Error getting cedent ",OOOO0O00OOO00OO00 ['cedent_type'])#line:1096
            _OOO0OOOOOO00OOOO0 =int (0 )#line:1097
            OOOO0O00OOO00OO00 ['num_cedent']=len (OOOO0O00OOO00OO00 ['defi'].get ('attributes'))#line:1102
            if (OOOO0O00OOO00OO00 ['defi'].get ('type')=='con'):#line:1103
                _OOO0OOOOOO00OOOO0 =(1 <<O00O0O0OO0O0OO0OO .data ["rows_count"])-1 #line:1104
            O00O0O0OO0O0OO0OO ._genvar (OOO00OOO0OO0O00OO ,OOOO0O00OOO00OO00 ,_OO000OOOOO0O0O000 ,_OOOO00OOO0O0O0O0O ,_OOO0OOOOOO00OOOO0 ,OOOO0O00OOO00OO00 ['defi'].get ('minlen'),OOOO0O00OOO00OO00 ['defi'].get ('maxlen'))#line:1105
    def _calc_all (OOOO0OO0O0O0O0000 ,**OO0O00OO0OO0OO000 ):#line:1108
        if "df"in OO0O00OO0OO0OO000 :#line:1109
            OOOO0OO0O0O0O0000 ._prep_data (OOOO0OO0O0O0O0000 .kwargs .get ("df"))#line:1110
        if not (OOOO0OO0O0O0O0000 ._initialized ):#line:1111
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1112
        else :#line:1113
            OOOO0OO0O0O0O0000 ._calculate (**OO0O00OO0OO0OO000 )#line:1114
    def _check_cedents (OOO00OOOOO00O0OO0 ,O00OOOO0OOO0O000O ,**OOO000O000O0OOO00 ):#line:1116
        OO000OO0OO000OOOO =True #line:1117
        if (OOO000O000O0OOO00 .get ('quantifiers',None )==None ):#line:1118
            print (f"Error: missing quantifiers.")#line:1119
            OO000OO0OO000OOOO =False #line:1120
            return OO000OO0OO000OOOO #line:1121
        if (type (OOO000O000O0OOO00 .get ('quantifiers'))!=dict ):#line:1122
            print (f"Error: quantifiers are not dictionary type.")#line:1123
            OO000OO0OO000OOOO =False #line:1124
            return OO000OO0OO000OOOO #line:1125
        for O0OO00O0O00000O0O in O00OOOO0OOO0O000O :#line:1127
            if (OOO000O000O0OOO00 .get (O0OO00O0O00000O0O ,None )==None ):#line:1128
                print (f"Error: cedent {O0OO00O0O00000O0O} is missing in parameters.")#line:1129
                OO000OO0OO000OOOO =False #line:1130
                return OO000OO0OO000OOOO #line:1131
            OOOOOOOO0O0OOOOO0 =OOO000O000O0OOO00 .get (O0OO00O0O00000O0O )#line:1132
            if (OOOOOOOO0O0OOOOO0 .get ('minlen'),None )==None :#line:1133
                print (f"Error: cedent {O0OO00O0O00000O0O} has no minimal length specified.")#line:1134
                OO000OO0OO000OOOO =False #line:1135
                return OO000OO0OO000OOOO #line:1136
            if not (type (OOOOOOOO0O0OOOOO0 .get ('minlen'))is int ):#line:1137
                print (f"Error: cedent {O0OO00O0O00000O0O} has invalid type of minimal length ({type(OOOOOOOO0O0OOOOO0.get('minlen'))}).")#line:1138
                OO000OO0OO000OOOO =False #line:1139
                return OO000OO0OO000OOOO #line:1140
            if (OOOOOOOO0O0OOOOO0 .get ('maxlen'),None )==None :#line:1141
                print (f"Error: cedent {O0OO00O0O00000O0O} has no maximal length specified.")#line:1142
                OO000OO0OO000OOOO =False #line:1143
                return OO000OO0OO000OOOO #line:1144
            if not (type (OOOOOOOO0O0OOOOO0 .get ('maxlen'))is int ):#line:1145
                print (f"Error: cedent {O0OO00O0O00000O0O} has invalid type of maximal length.")#line:1146
                OO000OO0OO000OOOO =False #line:1147
                return OO000OO0OO000OOOO #line:1148
            if (OOOOOOOO0O0OOOOO0 .get ('type'),None )==None :#line:1149
                print (f"Error: cedent {O0OO00O0O00000O0O} has no type specified.")#line:1150
                OO000OO0OO000OOOO =False #line:1151
                return OO000OO0OO000OOOO #line:1152
            if not ((OOOOOOOO0O0OOOOO0 .get ('type'))in (['con','dis'])):#line:1153
                print (f"Error: cedent {O0OO00O0O00000O0O} has invalid type. Allowed values are 'con' and 'dis'.")#line:1154
                OO000OO0OO000OOOO =False #line:1155
                return OO000OO0OO000OOOO #line:1156
            if (OOOOOOOO0O0OOOOO0 .get ('attributes'),None )==None :#line:1157
                print (f"Error: cedent {O0OO00O0O00000O0O} has no attributes specified.")#line:1158
                OO000OO0OO000OOOO =False #line:1159
                return OO000OO0OO000OOOO #line:1160
            for OOO000OO0O00000OO in OOOOOOOO0O0OOOOO0 .get ('attributes'):#line:1161
                if (OOO000OO0O00000OO .get ('name'),None )==None :#line:1162
                    print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO} has no 'name' attribute specified.")#line:1163
                    OO000OO0OO000OOOO =False #line:1164
                    return OO000OO0OO000OOOO #line:1165
                if not ((OOO000OO0O00000OO .get ('name'))in OOO00OOOOO00O0OO0 .data ["varname"]):#line:1166
                    print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} not in variable list. Please check spelling.")#line:1167
                    OO000OO0OO000OOOO =False #line:1168
                    return OO000OO0OO000OOOO #line:1169
                if (OOO000OO0O00000OO .get ('type'),None )==None :#line:1170
                    print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} has no 'type' attribute specified.")#line:1171
                    OO000OO0OO000OOOO =False #line:1172
                    return OO000OO0OO000OOOO #line:1173
                if not ((OOO000OO0O00000OO .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1174
                    print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} has unsupported type {OOO000OO0O00000OO.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1175
                    OO000OO0OO000OOOO =False #line:1176
                    return OO000OO0OO000OOOO #line:1177
                if (OOO000OO0O00000OO .get ('minlen'),None )==None :#line:1178
                    print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} has no minimal length specified.")#line:1179
                    OO000OO0OO000OOOO =False #line:1180
                    return OO000OO0OO000OOOO #line:1181
                if not (type (OOO000OO0O00000OO .get ('minlen'))is int ):#line:1182
                    if not (OOO000OO0O00000OO .get ('type')=='one'):#line:1183
                        print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} has invalid type of minimal length.")#line:1184
                        OO000OO0OO000OOOO =False #line:1185
                        return OO000OO0OO000OOOO #line:1186
                if (OOO000OO0O00000OO .get ('maxlen'),None )==None :#line:1187
                    print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} has no maximal length specified.")#line:1188
                    OO000OO0OO000OOOO =False #line:1189
                    return OO000OO0OO000OOOO #line:1190
                if not (type (OOO000OO0O00000OO .get ('maxlen'))is int ):#line:1191
                    if not (OOO000OO0O00000OO .get ('type')=='one'):#line:1192
                        print (f"Error: cedent {O0OO00O0O00000O0O} / attribute {OOO000OO0O00000OO.get('name')} has invalid type of maximal length.")#line:1193
                        OO000OO0OO000OOOO =False #line:1194
                        return OO000OO0OO000OOOO #line:1195
        return OO000OO0OO000OOOO #line:1196
    def _calculate (OO0OOOOOO00O00000 ,**OOO00O0O0OOO0OO0O ):#line:1198
        if OO0OOOOOO00O00000 .data ["data_prepared"]==0 :#line:1199
            print ("Error: data not prepared")#line:1200
            return #line:1201
        OO0OOOOOO00O00000 .kwargs =OOO00O0O0OOO0OO0O #line:1202
        OO0OOOOOO00O00000 .proc =OOO00O0O0OOO0OO0O .get ('proc')#line:1203
        OO0OOOOOO00O00000 .quantifiers =OOO00O0O0OOO0OO0O .get ('quantifiers')#line:1204
        OO0OOOOOO00O00000 ._init_task ()#line:1206
        OO0OOOOOO00O00000 .stats ['start_proc_time']=time .time ()#line:1207
        OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do']=[]#line:1208
        OO0OOOOOO00O00000 .task_actinfo ['cedents']=[]#line:1209
        if OOO00O0O0OOO0OO0O .get ("proc")=='CFMiner':#line:1212
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do']=['cond']#line:1213
            if OOO00O0O0OOO0OO0O .get ('target',None )==None :#line:1214
                print ("ERROR: no target variable defined for CF Miner")#line:1215
                return #line:1216
            if not (OO0OOOOOO00O00000 ._check_cedents (['cond'],**OOO00O0O0OOO0OO0O )):#line:1217
                return #line:1218
            if not (OOO00O0O0OOO0OO0O .get ('target')in OO0OOOOOO00O00000 .data ["varname"]):#line:1219
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1220
                return #line:1221
        elif OOO00O0O0OOO0OO0O .get ("proc")=='4ftMiner':#line:1223
            if not (OO0OOOOOO00O00000 ._check_cedents (['ante','succ'],**OOO00O0O0OOO0OO0O )):#line:1224
                return #line:1225
            _OO0O0000OO0OOOO00 =OOO00O0O0OOO0OO0O .get ("cond")#line:1227
            if _OO0O0000OO0OOOO00 !=None :#line:1228
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1229
            else :#line:1230
                O0OOO000OO0OOO00O =OO0OOOOOO00O00000 .cedent #line:1231
                O0OOO000OO0OOO00O ['cedent_type']='cond'#line:1232
                O0OOO000OO0OOO00O ['filter_value']=(1 <<OO0OOOOOO00O00000 .data ["rows_count"])-1 #line:1233
                O0OOO000OO0OOO00O ['generated_string']='---'#line:1234
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1236
                OO0OOOOOO00O00000 .task_actinfo ['cedents'].append (O0OOO000OO0OOO00O )#line:1237
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1241
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1242
        elif OOO00O0O0OOO0OO0O .get ("proc")=='NewAct4ftMiner':#line:1243
            _OO0O0000OO0OOOO00 =OOO00O0O0OOO0OO0O .get ("cond")#line:1246
            if _OO0O0000OO0OOOO00 !=None :#line:1247
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1248
            else :#line:1249
                O0OOO000OO0OOO00O =OO0OOOOOO00O00000 .cedent #line:1250
                O0OOO000OO0OOO00O ['cedent_type']='cond'#line:1251
                O0OOO000OO0OOO00O ['filter_value']=(1 <<OO0OOOOOO00O00000 .data ["rows_count"])-1 #line:1252
                O0OOO000OO0OOO00O ['generated_string']='---'#line:1253
                print (O0OOO000OO0OOO00O ['filter_value'])#line:1254
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1255
                OO0OOOOOO00O00000 .task_actinfo ['cedents'].append (O0OOO000OO0OOO00O )#line:1256
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('antv')#line:1257
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1258
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1259
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1260
        elif OOO00O0O0OOO0OO0O .get ("proc")=='Act4ftMiner':#line:1261
            _OO0O0000OO0OOOO00 =OOO00O0O0OOO0OO0O .get ("cond")#line:1264
            if _OO0O0000OO0OOOO00 !=None :#line:1265
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1266
            else :#line:1267
                O0OOO000OO0OOO00O =OO0OOOOOO00O00000 .cedent #line:1268
                O0OOO000OO0OOO00O ['cedent_type']='cond'#line:1269
                O0OOO000OO0OOO00O ['filter_value']=(1 <<OO0OOOOOO00O00000 .data ["rows_count"])-1 #line:1270
                O0OOO000OO0OOO00O ['generated_string']='---'#line:1271
                print (O0OOO000OO0OOO00O ['filter_value'])#line:1272
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1273
                OO0OOOOOO00O00000 .task_actinfo ['cedents'].append (O0OOO000OO0OOO00O )#line:1274
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1275
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1276
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1277
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1278
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1279
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1280
        elif OOO00O0O0OOO0OO0O .get ("proc")=='SD4ftMiner':#line:1281
            if not (OO0OOOOOO00O00000 ._check_cedents (['ante','succ','frst','scnd'],**OOO00O0O0OOO0OO0O )):#line:1284
                return #line:1285
            _OO0O0000OO0OOOO00 =OOO00O0O0OOO0OO0O .get ("cond")#line:1286
            if _OO0O0000OO0OOOO00 !=None :#line:1287
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1288
            else :#line:1289
                O0OOO000OO0OOO00O =OO0OOOOOO00O00000 .cedent #line:1290
                O0OOO000OO0OOO00O ['cedent_type']='cond'#line:1291
                O0OOO000OO0OOO00O ['filter_value']=(1 <<OO0OOOOOO00O00000 .data ["rows_count"])-1 #line:1292
                O0OOO000OO0OOO00O ['generated_string']='---'#line:1293
                OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1295
                OO0OOOOOO00O00000 .task_actinfo ['cedents'].append (O0OOO000OO0OOO00O )#line:1296
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('frst')#line:1297
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1298
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1299
            OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1300
        else :#line:1301
            print ("Unsupported procedure")#line:1302
            return #line:1303
        print ("Will go for ",OOO00O0O0OOO0OO0O .get ("proc"))#line:1304
        OO0OOOOOO00O00000 .task_actinfo ['optim']={}#line:1307
        OOOOO000O000OO000 =True #line:1308
        for O0000O0O0OOO0OOO0 in OO0OOOOOO00O00000 .task_actinfo ['cedents_to_do']:#line:1309
            try :#line:1310
                OO0O0O00OO00O0OO0 =OO0OOOOOO00O00000 .kwargs .get (O0000O0O0OOO0OOO0 )#line:1311
                if OO0O0O00OO00O0OO0 .get ('type')!='con':#line:1315
                    OOOOO000O000OO000 =False #line:1316
            except :#line:1318
                OOO0O0OOOOO0OO000 =1 <2 #line:1319
        if OO0OOOOOO00O00000 .options ['optimizations']==False :#line:1321
            OOOOO000O000OO000 =False #line:1322
        OOO00O0OO00O000OO ={}#line:1323
        OOO00O0OO00O000OO ['only_con']=OOOOO000O000OO000 #line:1324
        OO0OOOOOO00O00000 .task_actinfo ['optim']=OOO00O0OO00O000OO #line:1325
        print ("Starting to mine rules.")#line:1333
        OO0OOOOOO00O00000 ._start_cedent (OO0OOOOOO00O00000 .task_actinfo )#line:1334
        OO0OOOOOO00O00000 .stats ['end_proc_time']=time .time ()#line:1336
        print ("Done. Total verifications : "+str (OO0OOOOOO00O00000 .stats ['total_cnt'])+", rules "+str (OO0OOOOOO00O00000 .stats ['total_valid'])+",control number:"+str (OO0OOOOOO00O00000 .stats ['control_number'])+", times: prep "+str (OO0OOOOOO00O00000 .stats ['end_prep_time']-OO0OOOOOO00O00000 .stats ['start_prep_time'])+", processing "+str (OO0OOOOOO00O00000 .stats ['end_proc_time']-OO0OOOOOO00O00000 .stats ['start_proc_time']))#line:1339
        O0OOOO0OO0O0O0OO0 ={}#line:1340
        O000O0OO000O00O0O ={}#line:1341
        O000O0OO000O00O0O ["task_type"]=OOO00O0O0OOO0OO0O .get ('proc')#line:1342
        O000O0OO000O00O0O ["target"]=OOO00O0O0OOO0OO0O .get ('target')#line:1344
        O000O0OO000O00O0O ["self.quantifiers"]=OO0OOOOOO00O00000 .quantifiers #line:1345
        if OOO00O0O0OOO0OO0O .get ('cond')!=None :#line:1347
            O000O0OO000O00O0O ['cond']=OOO00O0O0OOO0OO0O .get ('cond')#line:1348
        if OOO00O0O0OOO0OO0O .get ('ante')!=None :#line:1349
            O000O0OO000O00O0O ['ante']=OOO00O0O0OOO0OO0O .get ('ante')#line:1350
        if OOO00O0O0OOO0OO0O .get ('succ')!=None :#line:1351
            O000O0OO000O00O0O ['succ']=OOO00O0O0OOO0OO0O .get ('succ')#line:1352
        if OOO00O0O0OOO0OO0O .get ('opts')!=None :#line:1353
            O000O0OO000O00O0O ['opts']=OOO00O0O0OOO0OO0O .get ('opts')#line:1354
        O0OOOO0OO0O0O0OO0 ["taskinfo"]=O000O0OO000O00O0O #line:1355
        O0OOO00O00OOO0O00 ={}#line:1356
        O0OOO00O00OOO0O00 ["total_verifications"]=OO0OOOOOO00O00000 .stats ['total_cnt']#line:1357
        O0OOO00O00OOO0O00 ["valid_rules"]=OO0OOOOOO00O00000 .stats ['total_valid']#line:1358
        O0OOO00O00OOO0O00 ["total_verifications_with_opt"]=OO0OOOOOO00O00000 .stats ['total_ver']#line:1359
        O0OOO00O00OOO0O00 ["time_prep"]=OO0OOOOOO00O00000 .stats ['end_prep_time']-OO0OOOOOO00O00000 .stats ['start_prep_time']#line:1360
        O0OOO00O00OOO0O00 ["time_processing"]=OO0OOOOOO00O00000 .stats ['end_proc_time']-OO0OOOOOO00O00000 .stats ['start_proc_time']#line:1361
        O0OOO00O00OOO0O00 ["time_total"]=OO0OOOOOO00O00000 .stats ['end_prep_time']-OO0OOOOOO00O00000 .stats ['start_prep_time']+OO0OOOOOO00O00000 .stats ['end_proc_time']-OO0OOOOOO00O00000 .stats ['start_proc_time']#line:1362
        O0OOOO0OO0O0O0OO0 ["summary_statistics"]=O0OOO00O00OOO0O00 #line:1363
        O0OOOO0OO0O0O0OO0 ["rules"]=OO0OOOOOO00O00000 .rulelist #line:1364
        O0O0O0OO0OOOOO0O0 ={}#line:1365
        O0O0O0OO0OOOOO0O0 ["varname"]=OO0OOOOOO00O00000 .data ["varname"]#line:1366
        O0O0O0OO0OOOOO0O0 ["catnames"]=OO0OOOOOO00O00000 .data ["catnames"]#line:1367
        O0OOOO0OO0O0O0OO0 ["datalabels"]=O0O0O0OO0OOOOO0O0 #line:1368
        OO0OOOOOO00O00000 .result =O0OOOO0OO0O0O0OO0 #line:1371
    def print_summary (O0OOOOO000O00OOO0 ):#line:1373
        print ("")#line:1374
        print ("CleverMiner task processing summary:")#line:1375
        print ("")#line:1376
        print (f"Task type : {O0OOOOO000O00OOO0.result['taskinfo']['task_type']}")#line:1377
        print (f"Number of verifications : {O0OOOOO000O00OOO0.result['summary_statistics']['total_verifications']}")#line:1378
        print (f"Number of rules : {O0OOOOO000O00OOO0.result['summary_statistics']['valid_rules']}")#line:1379
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O0OOOOO000O00OOO0.result['summary_statistics']['time_total']))}")#line:1380
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O0OOOOO000O00OOO0.result['summary_statistics']['time_prep']))}")#line:1382
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O0OOOOO000O00OOO0.result['summary_statistics']['time_processing']))}")#line:1383
        print ("")#line:1384
    def print_hypolist (OO0OOOOO000000OOO ):#line:1386
        OO0OOOOO000000OOO .print_rulelist ();#line:1387
    def print_rulelist (OO000O0O0O00O00OO ):#line:1389
        print ("")#line:1391
        print ("List of rules:")#line:1392
        if OO000O0O0O00O00OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1393
            print ("RULEID BASE  CONF  AAD    Rule")#line:1394
        elif OO000O0O0O00O00OO .result ['taskinfo']['task_type']=="CFMiner":#line:1395
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1396
        elif OO000O0O0O00O00OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1397
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1398
        else :#line:1399
            print ("Unsupported task type for rulelist")#line:1400
            return #line:1401
        for O00O0O000000OOOO0 in OO000O0O0O00O00OO .result ["rules"]:#line:1402
            O0O0000O00O0O0O00 ="{:6d}".format (O00O0O000000OOOO0 ["rule_id"])#line:1403
            if OO000O0O0O00O00OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1404
                O0O0000O00O0O0O00 =O0O0000O00O0O0O00 +" "+"{:5d}".format (O00O0O000000OOOO0 ["params"]["base"])+" "+"{:.3f}".format (O00O0O000000OOOO0 ["params"]["conf"])+" "+"{:+.3f}".format (O00O0O000000OOOO0 ["params"]["aad"])#line:1405
                O0O0000O00O0O0O00 =O0O0000O00O0O0O00 +" "+O00O0O000000OOOO0 ["cedents_str"]["ante"]+" => "+O00O0O000000OOOO0 ["cedents_str"]["succ"]+" | "+O00O0O000000OOOO0 ["cedents_str"]["cond"]#line:1406
            elif OO000O0O0O00O00OO .result ['taskinfo']['task_type']=="CFMiner":#line:1407
                O0O0000O00O0O0O00 =O0O0000O00O0O0O00 +" "+"{:5d}".format (O00O0O000000OOOO0 ["params"]["base"])+" "+"{:5d}".format (O00O0O000000OOOO0 ["params"]["s_up"])+" "+"{:5d}".format (O00O0O000000OOOO0 ["params"]["s_down"])#line:1408
                O0O0000O00O0O0O00 =O0O0000O00O0O0O00 +" "+O00O0O000000OOOO0 ["cedents_str"]["cond"]#line:1409
            elif OO000O0O0O00O00OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1410
                O0O0000O00O0O0O00 =O0O0000O00O0O0O00 +" "+"{:5d}".format (O00O0O000000OOOO0 ["params"]["base1"])+" "+"{:5d}".format (O00O0O000000OOOO0 ["params"]["base2"])+"    "+"{:.3f}".format (O00O0O000000OOOO0 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O00O0O000000OOOO0 ["params"]["deltaconf"])#line:1411
                O0O0000O00O0O0O00 =O0O0000O00O0O0O00 +"  "+O00O0O000000OOOO0 ["cedents_str"]["ante"]+" => "+O00O0O000000OOOO0 ["cedents_str"]["succ"]+" | "+O00O0O000000OOOO0 ["cedents_str"]["cond"]+" : "+O00O0O000000OOOO0 ["cedents_str"]["frst"]+" x "+O00O0O000000OOOO0 ["cedents_str"]["scnd"]#line:1412
            print (O0O0000O00O0O0O00 )#line:1414
        print ("")#line:1415
    def print_hypo (O00OO0O0O00OO0000 ,O0O000O00OO00O000 ):#line:1417
        O00OO0O0O00OO0000 .print_rule (O0O000O00OO00O000 )#line:1418
    def print_rule (OOO0OOO00O0O0OO0O ,OOOOO00000OOO0O00 ):#line:1421
        print ("")#line:1422
        if (OOOOO00000OOO0O00 <=len (OOO0OOO00O0O0OO0O .result ["rules"])):#line:1423
            if OOO0OOO00O0O0OO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1424
                print ("")#line:1425
                O00OOOO0O0OOO00O0 =OOO0OOO00O0O0OO0O .result ["rules"][OOOOO00000OOO0O00 -1 ]#line:1426
                print (f"Rule id : {O00OOOO0O0OOO00O0['rule_id']}")#line:1427
                print ("")#line:1428
                print (f"Base : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['base'])}  Relative base : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['rel_base'])}  CONF : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['conf'])}  AAD : {'{:+.3f}'.format(O00OOOO0O0OOO00O0['params']['aad'])}  BAD : {'{:+.3f}'.format(O00OOOO0O0OOO00O0['params']['bad'])}")#line:1429
                print ("")#line:1430
                print ("Cedents:")#line:1431
                print (f"  antecedent : {O00OOOO0O0OOO00O0['cedents_str']['ante']}")#line:1432
                print (f"  succcedent : {O00OOOO0O0OOO00O0['cedents_str']['succ']}")#line:1433
                print (f"  condition  : {O00OOOO0O0OOO00O0['cedents_str']['cond']}")#line:1434
                print ("")#line:1435
                print ("Fourfold table")#line:1436
                print (f"    |  S  |  ¬S |")#line:1437
                print (f"----|-----|-----|")#line:1438
                print (f" A  |{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold'][0])}|{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold'][1])}|")#line:1439
                print (f"----|-----|-----|")#line:1440
                print (f"¬A  |{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold'][2])}|{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold'][3])}|")#line:1441
                print (f"----|-----|-----|")#line:1442
            elif OOO0OOO00O0O0OO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1443
                print ("")#line:1444
                O00OOOO0O0OOO00O0 =OOO0OOO00O0O0OO0O .result ["rules"][OOOOO00000OOO0O00 -1 ]#line:1445
                print (f"Rule id : {O00OOOO0O0OOO00O0['rule_id']}")#line:1446
                print ("")#line:1447
                print (f"Base : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['base'])}  Relative base : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['max'])}  Histogram minimum : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['rel_min'])}")#line:1449
                print ("")#line:1450
                print (f"Condition  : {O00OOOO0O0OOO00O0['cedents_str']['cond']}")#line:1451
                print ("")#line:1452
                print (f"Histogram {O00OOOO0O0OOO00O0['params']['hist']}")#line:1453
            elif OOO0OOO00O0O0OO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1454
                print ("")#line:1455
                O00OOOO0O0OOO00O0 =OOO0OOO00O0O0OO0O .result ["rules"][OOOOO00000OOO0O00 -1 ]#line:1456
                print (f"Rule id : {O00OOOO0O0OOO00O0['rule_id']}")#line:1457
                print ("")#line:1458
                print (f"Base1 : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['base1'])} Base2 : {'{:5d}'.format(O00OOOO0O0OOO00O0['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O00OOOO0O0OOO00O0['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O00OOOO0O0OOO00O0['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O00OOOO0O0OOO00O0['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O00OOOO0O0OOO00O0['params']['ratioconf'])}")#line:1459
                print ("")#line:1460
                print ("Cedents:")#line:1461
                print (f"  antecedent : {O00OOOO0O0OOO00O0['cedents_str']['ante']}")#line:1462
                print (f"  succcedent : {O00OOOO0O0OOO00O0['cedents_str']['succ']}")#line:1463
                print (f"  condition  : {O00OOOO0O0OOO00O0['cedents_str']['cond']}")#line:1464
                print (f"  first set  : {O00OOOO0O0OOO00O0['cedents_str']['frst']}")#line:1465
                print (f"  second set : {O00OOOO0O0OOO00O0['cedents_str']['scnd']}")#line:1466
                print ("")#line:1467
                print ("Fourfold tables:")#line:1468
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1469
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1470
                print (f" A  |{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold1'][0])}|{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold2'][0])}|{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold2'][1])}|")#line:1471
                print (f"----|-----|-----|  ----|-----|-----|")#line:1472
                print (f"¬A  |{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold1'][2])}|{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold2'][2])}|{'{:5d}'.format(O00OOOO0O0OOO00O0['params']['fourfold2'][3])}|")#line:1473
                print (f"----|-----|-----|  ----|-----|-----|")#line:1474
            else :#line:1475
                print ("Unsupported task type for rule details")#line:1476
            print ("")#line:1480
        else :#line:1481
            print ("No such rule.")#line:1482
    def get_rulecount (OO00O0000000O00OO ):#line:1484
        return len (OO00O0000000O00OO .result ["rules"])#line:1485
    def get_fourfold (O00O0O0O0OOOOO0O0 ,O00OO0O0O00O0O0O0 ,order =0 ):#line:1487
        if (O00OO0O0O00O0O0O0 <=len (O00O0O0O0OOOOO0O0 .result ["rules"])):#line:1489
            if O00O0O0O0OOOOO0O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1490
                OOOO000O0O0OO0O0O =O00O0O0O0OOOOO0O0 .result ["rules"][O00OO0O0O00O0O0O0 -1 ]#line:1491
                return OOOO000O0O0OO0O0O ['params']['fourfold']#line:1492
            elif O00O0O0O0OOOOO0O0 .result ['taskinfo']['task_type']=="CFMiner":#line:1493
                print ("Error: fourfold for CFMiner is not defined")#line:1494
                return None #line:1495
            elif O00O0O0O0OOOOO0O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1496
                OOOO000O0O0OO0O0O =O00O0O0O0OOOOO0O0 .result ["rules"][O00OO0O0O00O0O0O0 -1 ]#line:1497
                if order ==1 :#line:1498
                    return OOOO000O0O0OO0O0O ['params']['fourfold1']#line:1499
                if order ==2 :#line:1500
                    return OOOO000O0O0OO0O0O ['params']['fourfold2']#line:1501
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1502
                return None #line:1503
            else :#line:1504
                print ("Unsupported task type for rule details")#line:1505
        else :#line:1506
            print ("No such rule.")#line:1507
    def get_hist (OOOO00OO0O000OOOO ,OOO0O00OOO00O00OO ):#line:1509
        if (OOO0O00OOO00O00OO <=len (OOOO00OO0O000OOOO .result ["rules"])):#line:1511
            if OOOO00OO0O000OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1512
                OO0000O0000O0O0O0 =OOOO00OO0O000OOOO .result ["rules"][OOO0O00OOO00O00OO -1 ]#line:1513
                return OO0000O0000O0O0O0 ['params']['hist']#line:1514
            elif OOOO00OO0O000OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1515
                print ("Error: SD4ft-Miner has no histogram")#line:1516
                return None #line:1517
            elif OOOO00OO0O000OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1518
                print ("Error: 4ft-Miner has no histogram")#line:1519
                return None #line:1520
            else :#line:1521
                print ("Unsupported task type for rule details")#line:1522
        else :#line:1523
            print ("No such rule.")#line:1524
    def get_quantifiers (O0O000O000O0OO0OO ,OOO0O0OOOOOOOO000 ,order =0 ):#line:1526
        if (OOO0O0OOOOOOOO000 <=len (O0O000O000O0OO0OO .result ["rules"])):#line:1528
            O00O0OO000OO0OOOO =O0O000O000O0OO0OO .result ["rules"][OOO0O0OOOOOOOO000 -1 ]#line:1529
            if O0O000O000O0OO0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1530
                return O00O0OO000OO0OOOO ['params']#line:1531
            elif O0O000O000O0OO0OO .result ['taskinfo']['task_type']=="CFMiner":#line:1532
                return O00O0OO000OO0OOOO ['params']#line:1533
            elif O0O000O000O0OO0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1534
                return O00O0OO000OO0OOOO ['params']#line:1535
            else :#line:1536
                print ("Unsupported task type for rule details")#line:1537
        else :#line:1538
            print ("No such rule.")#line:1539
