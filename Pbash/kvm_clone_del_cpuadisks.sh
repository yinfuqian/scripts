#!/bin/bash
#encoding=utf-8
bin=/usr/bin/virsh
filepath=/data/img/
qemupath=/etc/libvirt/qemu/
snapfile=/var/lib/libvirt/qemu/

##检查是否存在所需文件 路径
#file_exist_check() {
#        local filepath=$1  #调用时传参
#        if [ ! -d $filepath ];then 
#        	echo "【$filepath  not exist】"
#                echo "【miss tmeplate and important files,can not create kvm machine】"
#                exit
#        fi
#		}
#
#file_exist_check
#file_exist_check $snapfile 
#file_exist_check $bin

#创建机器
clone(){
	echo "
		******************************************************************
		*It was modify the setting file in this directory before creating*
		*   		First line is template machine                   *
		******************************************************************
		##################################################################
		#	    master must can connect temp machine                 #
		##################################################################
		"	
	while : 
	do
		read -p "import you tmeplete machine name:" mname
		if [ ! -f $qemupath$mname.xml ];then   #判断输入得机器是否存在
			echo "【$mname machine is not exit】"
			choose
			break
		else
			src_xml=/etc/libvirt/qemu/$mname.xml
			src_path=/data/img/$mname.qcow2
			read -p "import you tmeplete machine passwd:" passwd
			read -p "reimput you templete machine passwd " repasswd
			if [ $passwd = $repasswd ];then  
				$bin  start $mname > /dev/null 2>&1
				$bin  reboot $mname > /dev/null 2>&1 #通过尝试启动模板机器 来确定模板机是否可用
				if [ `echo $?` -eq  0 ];then
					echo "import success"
					vmfile #
					tmpmac=`virsh dumpxml $mname  |awk '{print $2}'|grep address=|awk -F "'" '{print $2}'` #得到模板机mac
					tmpipaddr=`arp -a|grep $tmpmac |grep -o '(.*)'|cut -d '(' -f2|cut -d ')' -f1`  #通过max得到模板机ip
					port=`netstat -tanlp |grep -E  'tcp.*LISTEN.*sshd' |egrep -v tcp6|awk '{print $4}' |awk -F ":" '{print $2}'` #得到sshd 端口
					ssh -p $port -t -t root@$tmpipaddr & 
					if [ $? -eq 0 ];
					then 
					echo "
#!/bin/bash
expect -c '
  spawn scp -P $port vm_setting root@$tmpipaddr:/home
  expect {
    \"*assword\" {set timeout 300; send $passwd\r\;}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
  }
expect eof '" > scp.sh
					sed -i -r "s/(ip=).*/\1$tmpipaddr/" scp.sh 
					sed -i -r "s/(passwd=).*/\1$passwd/" scp.sh 
					sed -i -r "s/(port=).*/\1$port/" scp.sh
					bash scp.sh
					create_domin 
					break
					else
						echo "yout temp machine port or ip can't not connect"
					fi	
				else 
					echo "【templete machine name error please reimport】"
					continue
				fi
			
			else
				echo "【passwd faild】"
				break
			fi
		fi
	done
	}

#得到创建机器时候指定ip所需要的文件
vmfile(){
	read -p "import you want to create domain number:" num
	if [ -z "$(echo $num | sed 's#[0-9]##g')" ];then  #判断输入得数字是否合法:num
		read -p "import you want to create domain name:" name
		read -p "import you kvm machine cpu set up:" cpus
		if [ -z "$(echo $cpus | sed 's#[0-9]##g')" ];then #nun
			read -p "import you kvm machine mem set up(GB):" mem
			if [ -z "$(echo $mem | sed 's#[0-9]##g')" ];then #num
			rm -rf kvm-tmp*.txt txt 
				tmpmac=`virsh dumpxml $mname  |awk '{print $2}'|grep address=|awk -F "'" '{print $2}'|awk -F ":" '{print $4":"$5":"$6}'` #mac地址后三位
				tmpip=`arp -a|grep $tmpmac|grep -o '(.*)'|cut -d '(' -f2|cut -d ')' -f1` #IP地址
				wanduan=`arp -a|grep $tmpmac|grep -o '(.*)'|cut -d '(' -f2|cut -d ')' -f1 |awk -F '.' '{print $1"."$2"."$3}'` #ip网段
				ip=`arp -a|grep $tmpmac|grep -o '(.*)'|cut -d '(' -f2|cut -d ')' -f1 |awk -F '.' '{print $4}'` #IP地址最后一位
				echo "$tmpmac   $tmpip  $name-0" > vm_setting   #将模板机-0重定向到setting文件中
				echo "$name-0   $tmpmac $cpus   $mem" > vm_list  #将模板机-0重定向到list文件中
				        for ((i=1; i<=$num;i++ )); do
				                        echo $name-$i >> kvm-tmp1.txt #名称
				                        openssl rand -hex 3 | sed 's/\(..\)/\1:/g; s/.$//' >> kvm-tmp2.txt #mac 地址
				                        echo $cpus >> kvm-tmp3.txt #cpu
				                        echo $mem >> kvm-tmp4.txt #内存
				        done
				                        paste kvm-tmp1.txt kvm-tmp2.txt kvm-tmp3.txt kvm-tmp4.txt >> vm_list #合并文件得到master.sh所需文件
				        
				        for ((i=$ip+1; i<=$ip+$num; i++)); do
				                echo "$wanduan.$i" >>kvm-tmp6.txt  #网段 + IP
				        done
				        awk '{print $2}' vm_list|egrep -v $tmpmac > kvm-tmpx.txt 
				        for mac in `cat kvm-tmpx.txt`;do
				                echo $mac >> kvm-tmp5.txt #mac 
				        done
				        paste kvm-tmp5.txt kvm-tmp6.txt  kvm-tmp1.txt >> vm_setting #合并模板机配置文件
					rm -rf kvm-tmp*.txt > /dev/null      
			else
				echo "【imput error】"
			fi
		else
			echo "【imput error】"
		fi                              
	else 
		echo "【imput error】"
	fi
	
}
scp(){
echo '
#!/bin/bash
expect -c "
  spawn scp -P '$port' vm_setting root@'$tmpipaddr':/home
  expect {
    \"*assword\" {set timeout 300; send \"'$passwd'\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
  }
  expect eof "' > scp.sh
sed -i -r "s/(ip=).*/\1$tmpipaddr/" scp.sh 
sed -i -r "s/(passwd=).*/\1$passwd/" scp.sh 
sed -i -r "s/(port=).*/\1$port/" scp.sh
}
#kvm创建
create_domin(){
	#从第二行循环遍历vmlist文件得到对应ip mac name 
	awk 'NR>1{print $0}' vm_list|while read line
	do
		newname=`echo $line|awk '{print $1}'` 
  		mac_addr=`echo $line|awk '{print $2}'`
  		newcpu=`echo $line|awk '{print $3}'`
  		newmem=`echo $line|awk '{print $4}'`
		uuid=`uuidgen`
		#新机器镜像文件
		new_path=$filepath\/${newname}.qcow2
		new_path_sed=$filepath\/${newname}.qcow2
		new_path_sed_sh=$(echo ${new_path_sed} |sed -e 's/\//\\\//g')  #将路径转义
		#新机器的xml文件
		new_xml=$qemupath\/${newname}.xml
		mem_kb=$((${newmem}*1024*1024))

		#模板文件复制
		cp  $src_path $new_path
		cp  $src_xml $new_xml

		#xml文件修改
		sed -r -i "s/(<name>).*(<\/name>)/\1$newname\2/" $new_xml
		sed -r -i "s/(<uuid>).*(<\/uuid>)/\1$uuid\2/" $new_xml
		sed -r -i "s/(<memory.*>).*(<\/memory>)/\1$mem_kb\2/" $new_xml
		sed -r -i "s/(currentMemory.*>).*(<\/currentMemory>)/\1$mem_kb\2/" $new_xml
		sed -r -i "s/(<vcpu.*).*(<\/vcpu>)/\1$newcpu\2/" $new_xml
		sed -r -i "1,/(source file=').*('\/>)/{s/(source file=').*('\/>)/\1$new_path_sed_sh\2/}" $new_xml #替换匹配到的第一个source file
		sed -r -i "s/(<mac address='..:..:..:).*('\/>)/\1$mac_addr\2/" $new_xml
		#根据条件创建虚拟机
		virts=`virsh list --all|awk '{if (NR>1) print $2}'` #已经存在的kvm 
		#遍历所有虚拟机跳过已经创建的
		for i in $virts; do 
			if [ $newname = $i ]; then
				echo "【$newname already be created】"
			else			
				$bin define $new_xml  &>/dev/null
				if [ $? -eq 0 ];then 	
					echo "【create successfully】"
				else 
					echo "【create faild】"
				fi
			fi
		done	
	done
choose
		}

# 删除机器
delete(){
	$bin list --all #列出所有机器
	read -p "import you want to delete domain name:" dname 
	virts=`virsh list --all|awk '{if (NR>1) print $2}'` #取出所有domin 名 称
		for i in $virts;do   
			if [ $dname = $i ];then
				virsh destroy $dname   &>/dev/null
				virsh undefine $dname  &>/dev/null
				#删除对应文件
				rm -rf $qemupath$dname.xml
				rm -rf $filepath$dname.qcow2
				echo "【$dname success define】"
				break
			else
				echo "【$dname was defined or imput error】"
			fi
		done
choose
	}

#列出所有机器
list(){
	$bin list --all
	choose
	}

#显示信息
show(){
	echo "
	*********************************
	*1:  cpus		2: mem  *	
	*3:ip and mac		4:return*
	*********************************"
	read -p "please choose what are you want to show:" show_choose
	read -p "please unput domin name  you want to show:" show_name
	case $show_choose in 
	1)
	$bin dominfo  |grep CPU #cpu信息
	choose
	;;
	2)
	#最大内存和已经使用内存
	mem=`virsh dominfo temp |grep mem |sed -n '1p' |awk '{print $3}'`
	used=`virsh dominfo temp |grep mem |sed -n '2p'|awk '{print $3}'`
	echo "【MAX MEM = $(($mem/1024))M】"
	echo "【USED MEM = $(($used/1024))M】"	
	choose
	;;
	3)
	#得到ip和mac地址
	mac=`virsh dumpxml  $show_name |awk '{print $2}'|grep address=|awk -F "'" '{print $2}'`
	ip=`arp -a|grep $mac |grep -o '(.*)'|cut -d '(' -f2|cut -d ')' -f1` #IP地址
	echo "【$show_name MAC is $mac】"
	echo "【$show_name IP is $ip】"
	choose
	;;
	4)
	choose
	;;
	*)
	echo "【imput error】"
	esac	
	}

# 磁盘扩容

disk(){
	echo "
	*******************************
	*  this disk only be add will *
	* will not be recase or remove*
	*******************************"
	read -p "please imput your domin name and will be add size(G):" domin size
	$bin start $domin
	echo $size
	for ((i=1; i<=$size;i++ )); do	
		qemu-img resize $filepath$domin.qcow2 +1G #一次加1G 循环添加闪现为输入的size 
	done
		$bin attach-disk $domin $filepath$domin.qcow2  vdb --live --cache=none --subdriver=qcow2  #添加vdb磁盘
	choose
	}


#cpu管理 只加不减
cpu(){
	 echo "
        *******************************
        *  this cpu only be add will *
        * will not be recase or remove*
        *******************************"
        read -p "please imput your domin name and will be add number):" domin number
	$bin setvcpus $domin $number --live  #添加cpu  
	if [ $? -eq 0 ];then
		echo "【add success】"
	else
		echo "【add filed cpu number not enough】" 
	fi
	choose
}

#创建快照
create_snapshots(){
        read -p "please imput your domin name):" sdomin
        virts=`virsh list --all|awk '{if (NR>1) print $2}'` #已经存在的kvm 
        #遍历所有虚拟机跳过已经创建的
        for i in $virts; do
                if [ $sdomin = $i ]; then
                        $bin snapshot-create $sdomin >> master.log &>/dev/null #将创建输出写入日志
                        if [ $? -eq 0 ];then
                                snapnum=`virsh snapshot-current  temp |grep creationTime |awk -F ">" '{print $2}'|awk -F "<" '{print $1}'` #得到快照编号
                        	snapfile='/var/lib/libvirt/qemu/snapshot/'
                                if [ ! -f $snapfile$sdmin\/$snapnum.xml ];then #判断是否存在快照文件
                                        echo "【create successfully】"
                                else
                                        echo "【create faild  can check [master.log]】"
                                fi
                         else
                                echo "【create filed】"

                        fi
		else 
				echo "【domin is not find】"
                fi
                done
	snapshot
	}

#删除快照
delete_snapshots(){
	read -p "please input domin name you want to handle:" snap_domin_name
	qemu-img info $filepath$snap_domin_name.qcow2  |grep "^[0-9]" > temp.txt  #得到所有快照信息
	cat temp.txt    
	read -p "please input num you want to delete:"  snap_num
	snap_choose=`cat temp.txt |grep "^[0-9]" |sed -n "\$snap_num p"|awk '{print $2}'`
	$bin snapshot-delete $snap_domin_name $snap_choose >> delete.log &>/dev/null
	if [ $? -eq 0 ];then 
		if [ ! -f $snapfile$snap_domin_name\/$snap_choose.xml ];then
			echo "【this snapshot was not be delete you can check log file[delete.log]】"
		else
			echo "【success this snapshost 】"
		fi 
	fi
	rm -rf temp.txt
	snapshot
}



#恢复快照
recover_snapshot(){
	read -p "please input domin name you want to handle:" recover_snap_name
	if [ ! -f $filepath $recover_snap_name ];then
		echo "【no search file in $filepath】"
		break
	else  
	qemu-img info $filepath$recover_snap_name.qcow2  |grep "^[0-9]" > temp.txt  #得到所有快照信息 
	cat temp.txt
	read -p "please input num you want to recover:"  recover_num 
	snap_choose_num=`cat temp.txt |grep "^[0-9]" |sed -n "\$recover_num p"|awk '{print $2}'` #得到snapshot名
	$bin snapshot-revert $recover_snap_name $snap_choose_num > recover.log   &>/dev/null#恢复操作
	        if [ $? -eq 0 ];then 
			recover_oldnum=`virsh snapshot-current  $recover_snap_name |grep creationTime |awk -F ">" '{print $2}'|awk -F "<" '{print $1}'` #得到恢复操作后的机器版本
			if [ $recover_oldnum = $snap_choose_num ];then  #将恢复后的版本号和快照版本号做对比
                        	echo "【recover succes】"
			else 
				echo "【recover faild】"
			fi
                else
                        echo "【handle this domin faild you can check log file [recover.log] 】"
                fi  
    		    rm -rf temp.txt

	fi
	snapshot
}

#快照管理
snapshot(){
	echo "
	*******************************
	*1:create             2:delete*
	*3:recover	      4:return*
	*******************************"
	read -p "please input your choose " snap_choose
	case $snap_choose in 
	1)
	create_snapshots
	;;
	2)
	delete_snapshots
	;;
	3)
	recover_snapshot
	;;
	4)
	choose
	;;
	*)
	echo "【imput error】"
	esac
}

choose(){
echo "
	******************************
        *1:clone       2:delete     *
        *3:list domins  4:show info  *
        *5:disk         6:cpu	     *
        *7:snapshot     0:exit 	     *
        ******************************
"
}
#file_exist_check
#vmlist=$1
#file_exist_check $vm_list "vm_list"
#file_exist_check $src_path "imagesfile"
#file_exist_check $src_xml "xml_file"
choose

while :
do
	read -p "please input your choose:" choose
	case $choose in
	1)
	clone
	;;
	2)
	delete
	;;
	3)
	list	
	;;
	4)
	show
	;;
	5)
	disk
	;;
	6)
	cpu
	;;
	7)
	snapshot
	;;
	0)
	exit
	;;
	*)
	echo "【input error please reinput】"
	esac
done
