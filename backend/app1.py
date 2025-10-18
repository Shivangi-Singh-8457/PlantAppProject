import schedule
import time
import os
import shutil
import glob
import MySQLdb
db = MySQLdb.connect("localhost", "root", "", "db",port_no)
print("db_connection established")
SERVER = "http://localhost:5000/"
BASE_DIRECTORY1 = ".//static/temp_images/"
BASE_DIRECTORY2 = ".//static/dataset/"

def func2():
	command1="select folder_id, img_index from temp_images where upvote>=5 and downvote>=upvote or report>=3"
	command2="delete from corrections where downvote>=3"
	command3="delete from temp_images where folder_id=%s and img_index=%s"
	mycursor=db.cursor()
	try:
		mycursor.execute(command1)
		result=mycursor.fetchall()
		print(result)
		fol_id=0
		img_ind=0
		query1="select leaf_division from temp where folder_id=%s" 
		query2="delete from temp_images where folder_id=%s and img_index=%s" 
		for it in result:
			print(it[0])
			mycursor.execute(query1,(it[0],))
			dirName=mycursor.fetchone()
			print("func2 dir="+dirName[0])
			mycursor.execute(query2,(it[0],it[1]))
			print("delete image db")
			os.remove(BASE_DIRECTORY1+dirName[0]+"/img_"+ str(it[1]) +".png")
			print("delete image")
		mycursor.execute(command2)
		print("delete corrections")	
		db.commit()	
	
	except:
		print("unable to delete")	

def func1():
	print("start checking")
	func2()
	print("returned")
	command1="select folder_id, img_index, upvote from temp_images where upvote>=5 and downvote<=3 and report<=2"
	mycursor=db.cursor()
	try:
		mycursor.execute(command1)
		result=mycursor.fetchall()
		print(result)
		print("run command1")	
		query1="select leaf_division from temp where folder_id=%s"
		query2="select folder_id from temp2 where leaf_division=%s"
		flag=False
		for it in result:
			mycursor.execute(query1,(it[0],))
			dirName=mycursor.fetchone()
			print("dir="+dirName[0])
			mycursor.execute(query2,(dirName[0],))
			res=mycursor.fetchone()
			print(res)
			if res is None:
				command2="select * from temp where leaf_division="+f"'{dirName[0]}' and upvote>=5 and downvote<=3 and report<=2 order by upvote desc"
				mycursor.execute(command2)
				res1=mycursor.fetchall()
				print(res1)
				if len(res1)!=0:
					print("in")
					item=res1[0]
					command3="insert into temp2(leaf_division, leaf_apices, leaf_bases, leaf_shape, leaf_margin, pattern) values("+f"'{item[1]}','{item[2]}','{item[3]}','{item[4]}','{item[5]}','{item[6]}')"	
					mycursor.execute(command3)
					print("move folder")
					command4="update users set upvotes=upvotes+"f"{item[10]} where user_id='{item[9]}'"
					mycursor.execute(command4)
					os.mkdir(BASE_DIRECTORY2 + dirName[0])
					shutil.move(BASE_DIRECTORY1+dirName[0]+"/img_"+str(it[1])+".png", BASE_DIRECTORY2+dirName[0])
					os.rename(BASE_DIRECTORY2+dirName[0]+"/img_"+str(it[1])+".png", BASE_DIRECTORY2+dirName[0]+"/img_1.png")
					print("move image1")
					flag=True
				print("out")
			else:
				os.rename(BASE_DIRECTORY1+dirName[0]+"/img_"+str(it[1])+".png", BASE_DIRECTORY1+dirName[0]+"/img_.png")
				list_of_files=glob.glob(BASE_DIRECTORY2 + dirName[0] + "/*")
				latest_file=max(list_of_files,key=os.path.getctime)
				#print(latest_file)
				basename=os.path.basename(latest_file)
				#print(basename)
				filename=os.path.splitext(basename)[0]
				#print(filename)
				cnt=int(filename.split("_")[1])
				#print(cnt)
				shutil.move(BASE_DIRECTORY1+dirName[0]+"/img_.png", BASE_DIRECTORY2+dirName[0])
				os.rename(BASE_DIRECTORY2+dirName[0]+"/img_.png", BASE_DIRECTORY2+dirName[0]+"/img_"+str(cnt+1)+".png")
				print("move image2")
				flag=True

			if flag:	
				command5="select user_id from temp where folder_id="+f"{it[0]}"
				mycursor.execute(command5)
				res=mycursor.fetchone()
				command6="update users set upvotes=upvotes+"f"{it[2]} where user_id='{res[0]}'"
				mycursor.execute(command6)
				command7="delete from temp_images where folder_id="f"{it[0]} and img_index={it[1]}"
				mycursor.execute(command7)
				if len(os.listdir(BASE_DIRECTORY1+dirName[0]))==0:
					os.remove(BASE_DIRECTORY1+dirName[0])
			print("now commit")		
			db.commit()	
			print("done")
	except:
		print("unable to move")	

schedule.every(1/2).minutes.do(func1)

while True:

	schedule.run_pending()
	time.sleep(1/2)

