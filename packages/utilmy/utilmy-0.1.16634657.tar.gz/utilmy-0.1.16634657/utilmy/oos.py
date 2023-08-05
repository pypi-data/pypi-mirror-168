# -*- coding: utf-8 -*-
"""# 
Doc::

    https://github.com/uqfoundation/pox/tree/master/pox


"""
import os, sys, time, datetime,inspect, json, yaml, gc, pandas as pd, numpy as np, glob


#################################################################
from utilmy.utilmy_base import log, log2

def help():
    """function help
    """
    from utilmy import help_create
    ss = help_create(__file__)
    print(ss)


#################################################################
###### TEST #####################################################
def test_all():
    """ python  utilmy/oos.py test_all
    """
    test_filecache()
    test_globglob()

    test0()
    # test2()
    test4()
    test5_os()
    test6_os()
    test7_os()



def test_globglob():
    import utilmy
    drepo, dtmp = utilmy.dir_testinfo()

    for path in ["folder/test/file1.txt","folder/test/tmp/1.txt","folder/test/tmp/myfile.txt",\
                "folder/test/tmp/record.txt","folder/test/tmp/part.parquet","folder/test/file2.txt",\
                "folder/test/file3.txt"]:

        os_makedirs(path)
        assert os.path.exists(path),"File doesn't exist"


    glob_glob(dirin="folder/**/*.txt")
    glob_glob(dirin="folder/**/*.txt",exclude="file2.txt,1")
    glob_glob(dirin="folder/**/*.txt",exclude="file2.txt,1",include_only="file")
    glob_glob(dirin="folder/**/*",nfiles=5)
    glob_glob(dirin="folder/**/*.txt",ndays_past=0,nmin_past=5,verbose=1)
    glob_glob(dirin="folder/",npool=1)
    glob_glob(dirin="folder/test/",npool=1)

    flist = ['folder/test/file.txt',
        'folder/test/file1.txt',
        'folder/test/file2.txt',
        'folder/test/file3.txt',
        'folder/test/tmp/1.txt',
        'folder/test/tmp/myfile.txt',
        'folder/test/tmp/record.txt']
    glob_glob(dirin="", file_list=flist)
    glob_glob(file_list=flist)
    glob_glob(file_list=flist,exclude="file2.txt,1",include_only="file")
    glob_glob(file_list=flist,exclude="file2.txt,1",include_only="file",npool=1)
    glob_glob(file_list=flist,exclude="file2.txt,1",include_only="file",npool=1)


def test_filecache():
    import utilmy
    drepo, dtmp = utilmy.direpo() , utilmy.os_get_dirtmp()

    fc = fileCache(dir_cache='test')
    data = [1,2 ,3, 4]
    fc.set( 'test', data )
    log(fc.get('test'))
    assert fc.get('test') == data, 'FAILED, file cache'



def test0():
    """function test0
    """
    import utilmy
    drepo, dtmp = utilmy.dir_testinfo()

    #logfull("log2")
    #logfull2("log5")


    #################
    os_makedirs('ztmp/ztmp2/myfile.txt')
    os_makedirs('ztmp/ztmp3/ztmp4')
    os_makedirs('/tmp/one/two')
    os_makedirs('/tmp/myfile')
    os_makedirs('/tmp/one/../mydir/')
    os_makedirs('./tmp/test')
    os.system("ls ztmp")

    path = ["/tmp/", "ztmp/ztmp3/ztmp4", "/tmp/", "./tmp/test","/tmp/one/../mydir/"]
    for p in path:
       f = os.path.exists(os.path.abspath(p))
       assert  f == True, "path " + p

    rev_stat = os_removedirs("ztmp/ztmp2")
    assert not rev_stat == False, "cannot delete root folder"


    ############
    res = os_system( f" ls . ",  doprint=True)
    log(res)
    res = os_system( f" ls . ",  doprint=False)
    assert os_get_os() == sys.platform



def test_create_testfiles():
    import utilmy
    drepo, dtmp = utilmy.dir_testinfo()

    from utilmy import to_file


    ss= """
    
    
    """
    to_file(ss,dtmp + "/test.txt" )



    ss ="""
    
    """
    to_file(ss,dtmp + "/test.txt" )



def test2():
    """function test2
    """
    import utilmy as uu
    drepo, dtmp = uu.dir_testinfo()

    test_create_testfiles()


    size_ = os_path_size()
    log("total size", size_)

    result_ = os_path_split("test/tmp/test.txt")
    log("result", result_)
    


    uu.to_file("Dummy text", dtmp + "/os_file_test.txt")
    os_file_check(dtmp + "/os_file_test.txt")
    res = z_os_search_fast(dtmp + "/os_file_test.txt", ["Dummy"],mode="regex")

    os_file_replacestring(findstr="text",replacestr="text_replace",
                          some_dir=dtmp + "/", pattern="*.*", dirlevel=2)

    os_copy_safe(drepo + "/testdata/tmp/test", drepo + "/testdata/tmp/test_copy/")



def test4():
    """function test4
    """
    import utilmy
    drepo, dtmp = utilmy.dir_testinfo()


    log(os_get_function_name())
    cwd = os.getcwd()
    #log(os_walk(cwd))
    cmd = ["pwd","whoami"]
    os_system_list(cmd, sleep_sec=0)
    ll = ["test_var"]
    globs = {}
    os_variable_init(ll,globs)
    os_variable_exist("test_var",globs)
    os_variable_check("other_var",globs,do_terminate=False)
    os_import(mod_name="pandas", globs=globs)
    os_variable_del(["test_var"], globs)

    log(os_variable_exist("test_var",globs))
    assert os.path.exists(dtmp + "/"),"Directory doesn't exist"



def test5_os():
    log(" os_copy")
    os_copy(dirfrom="folder/**/*.parquet", dirto="folder2/",

            mode='file',

            exclude="", include_only="",
            min_size_mb=0, max_size_mb=500000,
            ndays_past=-1, nmin_past=-1,  start_date='1970-01-02', end_date='2050-01-01',
            nfiles=99999999, verbose=0,

            dry=0
            )



def test6_os():

    #from utilmy import oos as m
    import utilmy as uu
    drepo, dtmp = uu.dir_testinfo()

    log("#######   os utils...")
    log(os_get_os())
    assert os_get_os() == sys.platform, "Platform mismatch"
    log(os_cpu_info())
    log(os_ram_info())
    log(os_getcwd())
    os_sleep_cpu(cpu_min=30, sleep=1, interval=5, verbose=True)

    c = {1, 3, "sdsfsdf"}
    log(os_sizeof(c, set()))


    log("#######   os_path_size() ..")
    size_ = os_path_size(drepo)
    assert not log("total size", size_) and size_> 10 , f"error {size_}"


    log("#######   os_path_split() ..")
    result_ = os_path_split(dtmp+"/test.txt")
    log("result", result_)


    log("#######   os_file_replacestring() ..")



    log("#######   os_walk() ..")
    cwd = os.getcwd()
    # log(os_walk(cwd))


    log("#######   os_copy_safe() ..")
    os_copy_safe(dtmp+"/test", dtmp+"/test_copy/")



    log("#######   z_os_search_fast() ..")
    with open(dtmp+"/os_search_test.txt", 'a') as file:
        file.write("Dummy text to test fast search string")
    res = z_os_search_fast(dtmp+"/os_search_test.txt", ["Dummy"],mode="regex")
    print(res)
    assert os.path.exists(dtmp+"/os_search_test.txt"),"File not found"



    log("#######   os_search_content() ..")
    uu.to_file("Dummy text to test fast search string", dtmp+"/os_search_content_test.txt", mode='a')
    # os_search_content(srch_pattern="fast", dir1=dtmp, file_pattern="*.txt")


    cwd = os.getcwd()
    '''TODO: for f in list_all["fullpath"]:
        KeyError: 'fullpath'
    res = os_search_content(srch_pattern= "Dummy text",dir1=os.path.join(cwd ,"tmp/test/"))
    log(res)
    '''


    log("#######   os_get_function_name() ..")
    log(os_get_function_name())



    log("#######   os_variables_test ..")
    ll = ["test_var"]
    globs = {}
    os_variable_init(ll,globs)
    os_variable_exist("test_var",globs)
    os_variable_check("other_var",globs,do_terminate=False)
    os_import(mod_name="pandas", globs=globs)
    os_variable_del(["test_var"], globs)
    log(os_variable_exist("test_var",globs))


    log("#######   os_system_list() ..")
    cmd = ["pwd","whoami"]
    os_system_list(cmd, sleep_sec=0)
    os_system("whoami", doprint=True)


    log("#######   os_file_check()")
    uu.to_file("test text to write to file", dtmp+"/file_test.txt", mode="a")
    os_file_check(dtmp+"/file_test.txt")



    log("#######   os utils...")
    uu.to_file("Dummy file to test os utils", dtmp+"/os_utils_test.txt")
    uu.to_file("Dummy text to test replace string", dtmp+"/os_test/os_file_test.txt")
    os_file_replacestring("text", "text_replace", dtmp+"/os_test/")

    #os_copy(os.path.join(os_getcwd(), "tmp/test"), os.path.join(os_getcwd(), "tmp/test/os_test"))
    os_removedirs(dtmp+"/os_test")
    assert ~os.path.exists(dtmp+"/os_test"),"Folder still found after removing"
    log(os_sizeof(["3434343", 343242, {3434, 343}], set()))



def test7_os():
    import  utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()

    log("\n#######", os_merge_safe)
    uu.to_file("""test input1""", dirtmp + "test1.txt" )
    uu.to_file("""test input2""", dirtmp + "test2.txt" )

    os_merge_safe(dirin_list=[dirtmp+'./*.txt'], dirout=dirtmp+"merge.txt")
    os_remove(    dirin=dirtmp+'test1.txt', ndays_past=-1)
    log(os_file_date_modified(dirin=dirtmp+'merge.txt'))

    flist = glob_glob(dirtmp)
    assert len(flist) < 2, flist



def test_os_module_uncache():
    import  utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()

    import sys
    old_modules = sys.modules.copy()
    exclude_mods = {"json.decoder"}
    excludes_prefixes = {exclude_mod.split('.', 1)[0] for exclude_mod in exclude_mods}
    os_module_uncache(exclude_mods)
    new_modules = sys.modules.copy()
    removed = []
    kept = []
    for module_name in old_modules:
        module_prefix = module_name.split('.', 1)[0]
        if (module_prefix in excludes_prefixes) and (module_name not in exclude_mods):
            assert module_name not in new_modules
            removed.append(module_name)
        else:
            assert module_name in new_modules
            if module_name in exclude_mods:
                kept.append(module_name)
    log("Successfully remove module cache: ", ", ".join(removed))
    log("Successfully kept: ", ", ".join(kept))



def test8():
    import utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()

    obj_dir = dirtmp+"/xtest*.txt"
    total_files = []
    for name in ("xtest1", "xtest2", "xtest3"):
        with open(dirtmp+"/{}.txt".format(name), "w") as f:
            f.write(name)
            total_files.append(f.name)

    # test dry remove
    before_files = glob.glob(obj_dir, recursive=True)
    os_remove(dirin=obj_dir,
              min_size_mb=0, max_size_mb=1,
              exclude="", include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=99999999,
              dry=1)
    cur_files = glob.glob(obj_dir, recursive=True)
    assert before_files == cur_files

    # test exclude
    excludes = [dirtmp+"xtest1.txt", dirtmp+"xtest2.txt"]
    print(excludes)
    os_remove(dirin=obj_dir,
              min_size_mb=0, max_size_mb=1,
              exclude=','.join(excludes), include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=99999999,
              dry=0)
    cur_files = glob.glob(obj_dir, recursive=True)
    for file in total_files:
        if file in excludes:
            assert file in cur_files
        else:
            assert file not in cur_files

    # test file num limit
    before_files = glob.glob(obj_dir, recursive=True)
    os_remove(dirin=obj_dir,
              min_size_mb=0, max_size_mb=1,
              exclude="", include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=1,
              dry=0)
    cur_files = glob.glob(obj_dir, recursive=True)
    assert len(before_files)-len(cur_files) == 1

    # test file size
    before_files = glob.glob(obj_dir, recursive=True)
    os_remove(dirin=obj_dir,
              min_size_mb=1, max_size_mb=2,
              exclude="", include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=1,
              dry=0)
    cur_files = glob.glob(obj_dir, recursive=True)
    assert len(before_files) == len(cur_files)



########################################################################################################
###### Fundamental functions ###########################################################################
def glob_glob(dirin="", file_list=[], exclude="", include_only="",
            min_size_mb=0, max_size_mb=500000,
            ndays_past=-1, nmin_past=-1,  start_date='1970-01-02', end_date='2050-01-01',
            nfiles=99999999, verbose=0, npool=1
    ):
    """ Advanced Glob filtering.
    Docs::

        dirin="": get the files in path dirin, works when file_list=[]
        file_list=[]: if file_list works, dirin will not work
        exclude=""   :
        include_only="" :
        min_size_mb=0
        max_size_mb=500000
        ndays_past=3000
        start_date='1970-01-01'
        end_date='2050-01-01'
        nfiles=99999999
        verbose=0
        npool=1: multithread not working

        https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio

    """
    import glob, copy, datetime as dt, time


    def fun_glob(dirin=dirin, file_list=file_list, exclude=exclude, include_only=include_only,
            min_size_mb=min_size_mb, max_size_mb=max_size_mb,
            ndays_past=ndays_past, nmin_past=nmin_past,  start_date=start_date, end_date=end_date,
            nfiles=nfiles, verbose=verbose,npool=npool):
        
        if dirin and not file_list:
            files = glob.glob(dirin, recursive=True)
            files = sorted(files)
        
        if file_list:
            files = file_list

        ####### Exclude/Include  ##################################################
        for xi in exclude.split(","):
            if len(xi) > 0:
                files = [  fi for fi in files if xi not in fi ]

        if include_only:
            tmp_list = [] # add multi files
            for xi in include_only.split(","):
                if len(xi) > 0:
                    tmp_list += [  fi for fi in files if xi in fi ]
            files = sorted(set(tmp_list))

        ####### size filtering  ##################################################
        if min_size_mb != 0 or max_size_mb != 0:
            flist2=[]
            for fi in files[:nfiles]:
                try :
                    if min_size_mb <= os.path.getsize(fi)/1024/1024 <= max_size_mb :   #set file size in Mb
                        flist2.append(fi)
                except : pass
            files = copy.deepcopy(flist2)

        #######  date filtering  ##################################################
        now    = time.time()
        cutoff = 0

        if ndays_past > -1 :
            cutoff = now - ( abs(ndays_past) * 86400)

        if nmin_past > -1 :
            cutoff = cutoff - ( abs(nmin_past) * 60  )

        if cutoff > 0:
            if verbose > 0 :
                print('now',  dt.datetime.utcfromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S"),
                       ',past', dt.datetime.utcfromtimestamp(cutoff).strftime("%Y-%m-%d %H:%M:%S") )
            flist2=[]
            for fi in files[:nfiles]:
                try :
                    t = os.stat( fi)
                    c = t.st_ctime
                    if c < cutoff:             # delete file if older than 10 days
                        flist2.append(fi)
                except : pass
            files = copy.deepcopy(flist2)

        ####### filter files between start_date and end_date  ####################
        if start_date and end_date:
            start_timestamp = time.mktime(time.strptime(str(start_date), "%Y-%m-%d"))
            end_timestamp   = time.mktime(time.strptime(str(end_date), "%Y-%m-%d"))
            flist2=[]
            for fi in files[:nfiles]:
                try:
                    t = os.stat( fi)
                    c = t.st_ctime
                    if start_timestamp <= c <= end_timestamp:
                        flist2.append(fi)
                except: pass
            files = copy.deepcopy(flist2)

        return files

    if npool ==  1:
        return fun_glob(dirin, file_list, exclude, include_only,
            min_size_mb, max_size_mb,
            ndays_past, nmin_past,  start_date, end_date,
            nfiles, verbose,npool)

    else :
        raise Exception('no working with npool>1')
        # from utilmy import parallel as par
        # input_fixed = {'exclude': exclude, 'include_only': include_only,
        #                'npool':1,
        #               }
        # if dirin and not file_list:
        #     fdir = [item for item in os.walk(dirin)] # os.walk(dirin, topdown=False)
        # if file_list:
        #     fdir = file_list
        # res  = par.multithread_run(fun_glob, input_list=fdir, input_fixed= input_fixed,
        #         npool=npool)
        # res  = sum(res) ### merge
        # return res



def os_remove(dirin="folder/**/*.parquet",
              min_size_mb=0, max_size_mb=1,
              exclude="", include_only="",
              ndays_past=1000, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=99999999,
              dry=0):

    """  Delete files bigger than some size

    """
    import os, sys, time, glob, datetime as dt

    dry = True if dry in {True, 1} else False

    flist2 = glob_glob(dirin, exclude=exclude, include_only=include_only,
            min_size_mb= min_size_mb, max_size_mb= max_size_mb,
            ndays_past=ndays_past, start_date=start_date, end_date=end_date,
            nfiles=nfiles,)


    print ('Nfiles', len(flist2))
    jj = 0
    for fi in flist2 :
        try :
            if not dry :
               os.remove(fi)
               jj = jj +1
            else :
               print(fi)
        except Exception as e :
            print(fi, e)

    if dry :  print('dry mode only')
    else :    print('deleted', jj)


def os_system(cmd, doprint=False):
  """ get values
       os_system( f"   ztmp ",  doprint=True)
  """
  import subprocess
  try :
    p          = subprocess.run( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, )
    mout, merr = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')
    if doprint:
      l = mout  if len(merr) < 1 else mout + "\n\nbash_error:\n" + merr
      print(l)

    return mout, merr
  except Exception as e :
    print( f"Error {cmd}, {e}")



#####################################################################################################
##### File I-O ######################################################################################
class fileCache(object):
    def __init__(self, dir_cache=None, ttl=None, size_limit=10000000, verbose=1):
        """ Simple cache system to store path --> list of files
            for S3 or HDFS

        """
        import tempfile, diskcache as dc

        dir_cache = tempfile.tempdir() if dir_cache is None else dir_cache
        dir_cache= dir_cache.replace("\\","/")
        dir_cache= dir_cache + "/filecache.db"
        self.dir_cache = dir_cache
        self.verbose = verbose
        self.size_limit = size_limit
        self.ttl = ttl if ttl is not None else 10

        cache = dc.Cache(dir_cache, size_limit= self.size_limit, timeout= self.ttl )
        if self.verbose:
            print('Cache size/limit', len(cache), self.size_limit )
        self.db = cache


    def get(self, path):
        path = path.replace("\\","/")
        return self.db.get(path, None)


    def set(self, path:str, flist:list, ttl=None):
        """

        expire (float) – seconds until item expires (default None, no expiry)

        """
        ttl = ttl if isinstance(ttl, int)  else self.ttl
        path = path.replace("\\","/")
        self.db.set(path, flist, expire=float(ttl), retry=True)



def os_copy(dirfrom="folder/**/*.parquet", dirto="",

            mode='file',

            exclude="", include_only="",
            min_size_mb=0, max_size_mb=500000,
            ndays_past=-1, nmin_past=-1,  start_date='1970-01-02', end_date='2050-01-01',
            nfiles=99999999, verbose=0,

            dry=0
            ) :
    """  Advance copy with filter.
    Docs::

          mode=='file'  :   file by file, very safe (can be very slow, not nulti thread)
          https://stackoverflow.com/questions/123198/how-to-copy-files



    """
    import os, shutil

    dry   = True if dry ==True or dry==1 else False
    flist = glob_glob(dirfrom, exclude=exclude, include_only=include_only,
            min_size_mb= min_size_mb, max_size_mb= max_size_mb,
            ndays_past=ndays_past, nmin_past=nmin_past, start_date=start_date, end_date=end_date,
            nfiles=nfiles,)

    if mode =='file':
        print ('Nfiles', len(flist))
        jj = 0
        for fi in flist :
            try :
                if not dry :
                   shutil.copy(fi, dirto)
                   jj = jj +1
                else :
                   print(fi)
            except Exception as e :
                print(fi, e)


        if dry :  print('dry mode only')
        else :    print('deleted', jj)

    elif mode =='dir':
         shutil.copytree(dirfrom, dirto, symlinks=False, ignore=None,  ignore_dangling_symlinks=False, dirs_exist_ok=False)



def os_copy_safe(dirin:str=None, dirout:str=None,  nlevel=5, nfile=5000, logdir="./", pattern="*", exclude="", force=False, sleep=0.5, cmd_fallback="",
                 verbose=True):  ###
    """ Copy safe, using callback command to re-connect network if broken
    Docs::


    """
    import shutil, time, os, glob

    flist = [] ; dirinj = dirin
    for j in range(nlevel):
        ztmp   = sorted( glob.glob(dirinj + "/" + pattern ) )
        dirinj = dirinj + "/*/"
        if len(ztmp) < 1 : break
        flist  = flist + ztmp

    flist2 = []
    for x in exclude.split(","):
        if len(x) <=1 : continue
        for t in flist :
            if  not x in t :
                flist2.append(t)
    flist = flist2

    log('n files', len(flist), dirinj, dirout ) ; time.sleep(sleep)
    kk = 0 ; ntry = 0 ;i =0
    for i in range(0, len(flist)) :
        fi  = flist[i]
        fi2 = fi.replace(dirin, dirout)

        if not fi.isascii(): continue
        if not os.path.isfile(fi) : continue

        if (not os.path.isfile(fi2) )  or force :
             kk = kk + 1
             if kk > nfile   : return 1
             if kk % 50 == 0  and sleep >0 : time.sleep(sleep)
             if kk % 10 == 0  and verbose  : log(fi2)
             os.makedirs(os.path.dirname(fi2), exist_ok=True)
             try :
                shutil.copy(fi, fi2)
                ntry = 0
                if verbose: log(fi2)
             except Exception as e:
                log(e)
                time.sleep(10)
                log(cmd_fallback)
                os.system(cmd_fallback)
                time.sleep(10)
                i = i - 1
                ntry = ntry + 1
    log('Scanned', i, 'transfered', kk)

### Alias
#os_copy = os_copy_safe


def os_merge_safe(dirin_list=None, dirout=None, nlevel=5, nfile=5000, nrows=10**8,
                  cmd_fallback = "umount /mydrive/  && mount /mydrive/  ", sleep=0.3):
    """function os_merge_safe
    Args:
        dirin_list:
        dirout:
        nlevel:
        nfile:
        nrows:
        cmd_fallback :
        sleep:
    Returns:

    """
    ### merge file in safe way
    nrows = 10**8
    flist = []
    for fi in dirin_list :
        flist = flist + glob.glob(fi)
    log(flist); time.sleep(2)

    os_makedirs(dirout)
    fout = open(dirout,'a')
    for fi in flist :
        log(fi)
        ii   = 0
        fin  = open(fi,'r')
        while True:
            try :
              ii = ii + 1
              if ii % 100000 == 0 : time.sleep(sleep)
              if ii > nrows : break
              x = fin.readline()
              if not x: break
              fout.write(x.strip()+"\n")
            except Exception as e:
              log(e)
              os.system(cmd_fallback)
              time.sleep(10)
              fout.write(x.strip()+"\n")
        fin.close()


def os_removedirs(path, verbose=False):
    """  issues with no empty Folder
    # Delete everything reachable from the directory named in 'top',
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it could delete all your disk files.
    """
    if len(path) < 3 :
        print("cannot delete root folder")
        return False

    import os
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            try :
              os.remove(os.path.join(root, name))
              if verbose: log(name)
            except Exception as e :
              log('error', name, e)

        for name in dirs:
            try :
              os.rmdir(os.path.join(root, name))
              if verbose: log(name)
            except  Exception as e:
              log('error', name, e)

    try :
      os.rmdir(path)
    except: pass
    return True


def os_makedirs(dir_or_file):
    """function os_makedirs
    Args:
        dir_or_file:
    Returns:

    """
    if os.path.isfile(dir_or_file) or "." in dir_or_file.split("/")[-1] :
        os.makedirs(os.path.dirname(os.path.abspath(dir_or_file)), exist_ok=True)
        f = open(dir_or_file,'w')
        f.close()
    else :
        os.makedirs(os.path.abspath(dir_or_file), exist_ok=True)



def os_getcwd():
    """  os.getcwd() This is for Windows Path normalized As Linux path /

    """
    root = os.path.abspath(os.getcwd()).replace("\\", "/") + "/"
    return  root


def os_system_list(ll, logfile=None, sleep_sec=10):
   """function os_system_list
   Args:
       ll:
       logfile:
       sleep_sec:
   Returns:

   """
   ### Execute a sequence of cmd
   import time, sys
   n = len(ll)
   for ii,x in enumerate(ll):
        try :
          log(x)
          if sys.platform == 'win32' :
             cmd = f" {x}   "
          else :
             cmd = f" {x}   2>&1 | tee -a  {logfile} " if logfile is not None else  x

          os.system(cmd)

          # tx= sum( [  ll[j][0] for j in range(ii,n)  ]  )
          # log(ii, n, x,  "remaining time", tx / 3600.0 )
          #log('Sleeping  ', x[0])
          time.sleep(sleep_sec)
        except Exception as e:
            log(e)


def os_file_date_modified(dirin, fmt="%Y%m%d-%H:%M", timezone='Asia/Tokyo'):
    """last modified date
    """
    import datetime
    from pytz import timezone as tzone
    try :
        mtime  = os.path.getmtime(dirin)
        mtime2 = datetime.datetime.utcfromtimestamp(mtime)
        mtime2 = mtime2.astimezone(tzone(timezone))
        return mtime2.strftime(fmt)
    except:
        return ""


def os_process_list():
    """  List of processes
    #ll = os_process_list()
    #ll = [t for t in ll if 'root' in t and 'python ' in t ]
    ### root   ....  python run
    """
    import subprocess
    ps = subprocess.Popen('ps -ef', shell=True, stdout=subprocess.PIPE)
    ll = ps.stdout.readlines()
    ll = [ t.decode().replace("\n", "") for t in ll ]
    return ll


def os_path_size(path = '.'):
    """function os_path_size
    Args:
        path :
    Returns:

    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def os_path_split(fpath:str=""):
    """function os_path_split
    Args:
        fpath ( str ) :
    Returns:

    """
    #### Get path split
    fpath = fpath.replace("\\", "/")
    if fpath[-1] == "/":
        fpath = fpath[:-1]

    parent = "/".join(fpath.split("/")[:-1])
    fname  = fpath.split("/")[-1]
    if "." in fname :
        ext = ".".join(fname.split(".")[1:])
    else :
        ext = ""

    return parent, fname, ext



def os_file_replacestring(findstr, replacestr, some_dir, pattern="*.*", dirlevel=1):
    """ #fil_replacestring_files("logo.png", "logonew.png", r"D:/__Alpaca__details/aiportfolio",
        pattern="*.html", dirlevel=5  )
    """
    def os_file_replacestring1(find_str, rep_str, file_path):
        """replaces all find_str by rep_str in file file_path"""
        import fileinput

        file1 = fileinput.FileInput(file_path, inplace=True, backup=".bak")
        for line in file1:
            line = line.replace(find_str, rep_str)
            sys.stdout.write(line)
        file1.close()
        print(("OK: " + format(file_path)))


    list_file = os_walk(some_dir, pattern=pattern, dirlevel=dirlevel)
    list_file = list_file['file']
    for file1 in list_file:
        os_file_replacestring1(findstr, replacestr, file1)



def os_file_check(fpath:str):
   """Check file stat info
   """
   import os, time

   flist = glob_glob(fpath)
   flag = True
   for fi in flist :
       try :
           log(fi,  os.stat(fi).st_size*0.001, time.ctime(os.path.getmtime(fi)) )
       except :
           log(fi, "Error File Not exist")
           flag = False
   return flag



def os_walk(path, pattern="*", dirlevel=50):
    """ dirlevel=0 : root directory
        dirlevel=1 : 1 path below

    """
    import fnmatch, os, numpy as np

    matches = {'file':[], 'dir':[]}
    dir1    = path.replace("\\", "/").rstrip("/")
    num_sep = dir1.count("/")

    for root, dirs, files in os.walk(dir1):
        root = root.replace("\\", "/")
        for fi in files :
            if root.count("/") > num_sep + dirlevel: continue
            matches['file'].append(os.path.join(root, fi).replace("\\","/"))

        for di in dirs :
            if root.count("/") > num_sep + dirlevel: continue
            matches['dir'].append(os.path.join(root, di).replace("\\","/") + "/")

    ### Filter files
    matches['file'] = [ t for t in fnmatch.filter(matches['file'], pattern) ]
    return  matches




#######################################################################################################
##### OS, config ######################################################################################
def os_monkeypatch_help():
    """function os_monkeypatch_help
    Args:
    Returns:

    """
    print( """
    https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
    
    
    """)


def os_module_uncache(exclude='os.system'):
    """Remove package modules from cache except excluded ones.
       On next import they will be reloaded.  Useful for monkey patching
    Args:
        exclude (iter<str>): Sequence of module paths.
        https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
    """
    import sys
    pkgs = []
    for mod in exclude:
        pkg = mod.split('.', 1)[0]
        pkgs.append(pkg)

    to_uncache = []
    for mod in sys.modules:
        if mod in exclude:
            continue

        if mod in pkgs:
            to_uncache.append(mod)
            continue

        for pkg in pkgs:
            if mod.startswith(pkg + '.'):
                to_uncache.append(mod)
                break

    for mod in to_uncache:
        del sys.modules[mod]


def os_import(mod_name="myfile.config.model", globs=None, verbose=True):
    """function os_import
    Args:
        mod_name:
        globs:
        verbose:
    Returns:

    """
    ### Import in Current Python Session a module   from module import *
    ### from mod_name import *
    module = __import__(mod_name, fromlist=['*'])
    if hasattr(module, '__all__'):
        all_names = module.__all__
    else:
        all_names = [name for name in dir(module) if not name.startswith('_')]

    all_names2 = []
    no_list    = ['os', 'sys' ]
    for t in all_names :
        if t not in no_list :
          ### Mot yet loaded in memory  , so cannot use Global
          #x = str( globs[t] )
          #if '<class' not in x and '<function' not in x and  '<module' not in x :
          all_names2.append(t)
    all_names = all_names2

    if verbose :
      print("Importing: ")
      for name in all_names :
         print( f"{name}=None", end=";")
      print("")
    globs.update({name: getattr(module, name) for name in all_names})







###################################################################################################
def z_os_search_fast(fname, texts=None, mode="regex/str"):
    """function z_os_search_fast
    Args:
        fname:
        texts:
        mode:
    Returns:

    """
    import re
    if texts is None:
        texts = ["myword"]

    res = []  # url:   line_id, match start, line
    enc = "utf-8"
    fname = os.path.abspath(fname)
    try:
        if mode == "regex":
            texts = [(text, re.compile(text.encode(enc))) for text in texts]
            for lineno, line in enumerate(open(fname, "rb")):
                for text, textc in texts:
                    found = re.search(textc, line)
                    if found is not None:
                        try:
                            line_enc = line.decode(enc)
                        except UnicodeError:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found.start(), line_enc))

        elif mode == "str":
            texts = [(text, text.encode(enc)) for text in texts]
            for lineno, line in enumerate(open(fname, "rb")):
                for text, textc in texts:
                    found = line.find(textc)
                    if found > -1:
                        try:
                            line_enc = line.decode(enc)
                        except UnicodeError:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found, line_enc))

    except IOError as xxx_todo_changeme:
        (_errno, _strerror) = xxx_todo_changeme.args
        print("permission denied errors were encountered")

    except re.error:
        print("invalid regular expression")

    return res



def os_search_content(srch_pattern=None, mode="str", dir1="", file_pattern="*.*", dirlevel=1):
    """  search inside the files

    """
    import pandas as pd
    if srch_pattern is None:
        srch_pattern = ["from ", "import "]

    list_all = os_walk(dir1, pattern=file_pattern, dirlevel=dirlevel)
    ll = []
    for f in list_all["fullpath"]:
        ll = ll + z_os_search_fast(f, texts=srch_pattern, mode=mode)
    df = pd.DataFrame(ll, columns=["search", "filename", "lineno", "pos", "line"])
    return df








###################################################################################################
def os_variable_init(ll, globs):
    """function os_variable_init
    Args:
        ll:
        globs:
    Returns:

    """
    for x in ll :
        try :
          globs[x]
        except :
          globs[x] = None


def os_variable_exist(x ,globs, msg="") :
    """function os_variable_exist
    Args:
        x:
        globs:
        msg:
    Returns:

    """
    x_str = str(globs.get(x, None))
    if "None" in x_str:
        log("Using default", x)
        return False
    else :
        log("Using ", x)
        return True


def os_variable_check(ll, globs=None, do_terminate=True):
  """function os_variable_check
  Args:
      ll:
      globs:
      do_terminate:
  Returns:

  """
  import sys
  for x in ll :
      try :
         a = globs[x]
         if a is None : raise Exception("")
      except :
          log("####### Vars Check,  Require: ", x  , "Terminating")
          if do_terminate:
                 sys.exit(0)


def os_variable_del(varlist, globx):
  """function os_clean_memory
  Args:
      varlist:
      globx:
  Returns:

  """
  for x in varlist :
    try :
       del globx[x]
       gc.collect()
    except : pass


def os_sizeof(o, ids, hint=" deep_getsizeof(df_pd, set()) "):
    """ Find the memory footprint of a Python object
    Docs::

        deep_getsizeof(df_pd, set())
        The sys.getsizeof function does a shallow size of only. It counts each
        object inside a container as pointer only regardless of how big it
    """
    from collections import Mapping, Container
    from sys import getsizeof

    _ = hint

    d = os_sizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, str):
        r = r

    if isinstance(o, Mapping):
        r = r + sum(d(k, ids) + d(v, ids) for k, v in o.items())

    if isinstance(o, Container):
        r = r + sum(d(x, ids) for x in o)

    return r * 0.0000001


def os_get_function_name():
    """function os_get_function_name
    Args:
    Returns:

    """
    ### Get ane,
    import sys, socket
    ss = str(os.getpid()) # + "-" + str( socket.gethostname())
    ss = ss + "," + str(__name__)
    try :
        ss = ss + "," + __class__.__name__
    except :
        ss = ss + ","
    ss = ss + "," + str(  sys._getframe(1).f_code.co_name)
    return ss






###################################################################################################
def os_get_os():
    """function os_platform_os
    Args:
    Returns:

    """
    #### get linux or windows
    return sys.platform


def os_get_ip():
    """function os_platform_ip
    Args:
    Returns:

    """
    ### IP
    pass


def os_cpu_info():
    """ get info on CPU  : nb of cpu, usage
    Docs:

         https://stackoverflow.com/questions/9229333/how-to-get-overall-cpu-usage-e-g-57-on-linux
    """
    ncpu= os.cpu_count()

    cmd = """ top -bn1 | grep "Cpu(s)" |  sed "s/.*, *\([0-9.]*\)%* id.*/\1/" |  awk '{print 100 - $1"%"}'  """
    cpu_usage = os_system(cmd)


    cmd = """ awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1) "%"; }' <(grep 'cpu ' /proc/stat) <(sleep 1;grep 'cpu ' /proc/stat) """
    cpu_usage = os_system(cmd)


def os_ram_info():
    """ Get total memory and memory usage in linux
    """
    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
        ret['free'] = tmp
        ret['used'] = int(ret['total']) - int(ret['free'])
    return ret


def os_sleep_cpu(cpu_min=30, sleep=10, interval=5, msg= "", verbose=True):
    """function os_sleep_cpu
    Docs::

        Args:
            cpu_min:
            sleep:
            interval:
            msg:
            verbose:
        Returns:
    """
    #### Sleep until CPU becomes normal usage
    import psutil, time
    aux = psutil.cpu_percent(interval=interval)  ### Need to call 2 times
    while aux > cpu_min:
        ui = psutil.cpu_percent(interval=interval)
        aux = 0.5 * (aux +  ui)
        if verbose : log( 'Sleep sec', sleep, ' Usage %', aux, ui, msg )
        time.sleep(sleep)
    return aux



def os_wait_processes(nhours=7):
    """function os_wait_processes
    Args:
        nhours:
    Returns:

    """
    t0 = time.time()
    while (time.time() - t0 ) < nhours * 3600 :
       ll = os_process_list()
       if len(ll) < 2 : break   ### Process are not running anymore
       log("sleep 30min", ll)
       time.sleep(3600* 0.5)




###################################################################################################
###### HELP ######################################################################################
def aaa_bash_help():
    """ Shorcuts for Bash
    Docs::


        --  Glob in Bash
        setopt extendedglob
        ls *(<tab>                                                    # to get help regarding globbing
        rm ../debianpackage(.)                                        # remove files only
        ls -d *(/)                                                    # list directories only
        ls /etc/*(@)                                                  # list symlinks only
        ls -l *.(png|jpg|gif)                                         # list pictures only
        ls *(*)                                                       # list executables only
        ls /etc/**/zsh                                                # which directories contain 'zsh'?
        ls **/*(-@)                                                   # list dangling symlinks ('**' recurses down directory trees)
        ls foo*~*bar*                                                 # match everything that starts with foo but doesn't contain bar
        ls *(e:'file $REPLY | grep -q JPEG':)                         # match all files of which file says that they are JPEGs
        ls -ldrt -- *(mm+15)                                          # List all files older than 15mins
        ls -ldrt -- *(.mm+15)                                         # List Just regular files
        ls -ld /my/path/**/*(D@-^@)                                   # List the unbroken sysmlinks under a directory.
        ls -Lldrt -- *(-mm+15)                                        # List the age of the pointed to file for symlinks
        ls -l **/README                                               # Search for `README' in all Subdirectories
        ls -l foo<23->                                                # List files beginning at `foo23' upwards (foo23, foo24, foo25, ..)
        ls -l 200406{04..10}*(N)                                      # List all files that begin with the date strings from June 4 through June 9 of 2004
        ls -l 200306<4-10>.*                                          # or if they are of the form 200406XX (require ``setopt extended_glob'')
        ls -l *.(c|h)                                                 # Show only all *.c and *.h - Files
        ls -l *(R)                                                    # Show only world-readable files
        ls -fld *(OL)                                                 # Sort the output from `ls -l' by file size
        ls -fl *(DOL[1,5])                                            # Print only 5 lines by "ls" command (like ``ls -laS | head -n 5'')
        ls -l *(G[users])                                             # Show only files are owned from group `users'
        ls *(L0f.go-w.)                                               # Show only empty files which nor `group' or `world writable'
        ls *.c~foo.c                                                  # Show only all *.c - files and ignore `foo.c'
        print -rl /home/me/**/*(D/e{'reply=($REPLY/*(N[-1]:t))'})     # Find all directories, list their contents and output the first item in the above list
        print -rl /**/*~^*/path(|/*)                                  # Find command to search for directory name instead of basename
        print -l ~/*(ND.^w)                                           # List files in the current directory are not writable by the owner
        print -rl -- *(Dmh+10^/)                                      # List all files which have not been updated since last 10 hours
        print -rl -- **/*(Dom[1,10])                                  # List the ten newest files in directories and subdirs (recursive)
        print -rl -- /path/to/dir/**/*(D.om[5,10])                    # Display the 5-10 last modified files
        print -rl -- **/*.c(D.OL[1,10]:h) | sort -u                   # Print the path of the directories holding the ten biggest C regular files in the current directory and subdirectories.
        setopt dotglob ; print directory/**/*(om[1])                  # Find most recent file in a directory
        for a in ./**/*\ *(Dod); do mv $a ${a:h}/${a:t:gs/ /_}; done  # Remove spaces from filenames


    """
    pass








###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



def zz_os_remove_file_past(dirin="folder/**/*.parquet", ndays_past=20, nfiles=1000000, exclude="", dry=1) :
    """  Delete files older than ndays.


    """
    import os, sys, time, glob, datetime as dt

    dry = True if dry ==True or dry==1 else False

    files = glob.glob(dirin, recursive=True)
    files = sorted(files)
    for exi in exclude.split(","):
        if len(exi) > 0:
           files = [  fi for fi in files if exi not in fi ]

    now = time.time()
    cutoff = now - ( abs(ndays_past) * 86400)
    print('now',   dt.datetime.utcfromtimestamp(now).strftime("%Y-%m-%d"),
          ',past', dt.datetime.utcfromtimestamp(cutoff).strftime("%Y-%m-%d") )
    flist2=[]
    for fi in files[:nfiles]:
        try :
          t = os.stat( fi)
          c = t.st_ctime
          # delete file if older than 10 days
          if c < cutoff:
            flist2.append(fi)
        except : pass

    print ('Nfiles', len(flist2))
    jj = 0
    for fi in flist2 :
        try :
            if not dry :
               os.remove(fi)
               jj = jj +1
            else :
               print(fi)
        except Exception as e :
            print(fi, e)

    if dry :  print('dry mode only')
    else :    print('deleted', jj)



