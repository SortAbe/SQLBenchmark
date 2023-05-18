#!/bin/env python3
#Abrahan Diaz
#Version 0.8


import random
import re
import time
import mysql.connector

class Filler:
	cnx = mysql.connector.connect(
		host='209.133.192.178',
		user='py',
		password='password123!',
		database='University',
		port=7707
	)
	cursor = cnx.cursor()
	departmentList = []
	femaleNames = []
	maleNames = []
	lastNames = []

	def __init__(self):
		#get deparments
		query = 'SELECT * FROM department'
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		for row in results:
			self.departmentList.append(row[0])
		#get names
		with open('./names/female.names', 'r') as femf:
			lines = femf.readlines()
			for line in lines:
				self.femaleNames.append(line)
		with open('./names/male.names', 'r') as malf:
			lines = malf.readlines()
			for line in lines:
				self.maleNames.append(line)
		with open('./names/last.names', 'r') as lasf:
			lines = lasf.readlines()
			for line in lines:
				self.lastNames.append(line)

	def fillFemales(self, rows=1000):
		flen = len(self.femaleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.femaleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO student (firstName, lastName, gender, dept_name, credits) VALUES (%s, %s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.femaleNames[i%flen].strip(), self.lastNames[i%llen].strip(), True, self.departmentList[i%dlen].strip() , credit)
			self.cursor.execute(sql, data)
		self.cnx.commit()
		
	def fillFemalesT(self, rows=100):
		flen = len(self.femaleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.femaleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO instructor (firstName, lastName, gender, dept_name) VALUES (%s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.femaleNames[i%flen].strip(), self.lastNames[i%llen].strip(), True, self.departmentList[i%dlen].strip())
			self.cursor.execute(sql, data)
		self.cnx.commit()

	def fillMales(self, rows=1000):
		mlen = len(self.maleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.maleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO student (firstName, lastName, gender, dept_name, credits) VALUES (%s, %s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.maleNames[i%mlen].strip(), self.lastNames[i%llen].strip(), False, self.departmentList[i%dlen].strip() , credit)
			self.cursor.execute(sql, data)
		self.cnx.commit()
	
	def fillMalesT(self, rows=100):
		mlen = len(self.maleNames)
		llen = len(self.lastNames)
		dlen = len(self.departmentList)
		random.shuffle(self.maleNames)
		random.shuffle(self.lastNames)
		random.shuffle(self.departmentList)
		sql = "INSERT INTO instructor (firstName, lastName, gender, dept_name) VALUES (%s, %s, %s, %s)"
		for i in range(rows):
			credit = random.choice(range(60))	
			data = (self.maleNames[i%mlen].strip(), self.lastNames[i%llen].strip(), False, self.departmentList[i%dlen].strip())
			self.cursor.execute(sql, data)
		self.cnx.commit()

	def class_(self, year=2023, semester='Spring'):
		self.cursor.execute('SELECT COUNT(*) FROM instructor;')
		amount = self.cursor.fetchall()[0][0] * 3
		self.cursor.execute('SELECT course.course_id, course.dept_name, department.building  FROM course JOIN department ON course.dept_name = department.dept_name ORDER BY department.building;')
		view = self.cursor.fetchall()
		building = None
		room_no = 0
		sql = 'INSERT INTO class (course_id, semester, year, building, room_no) VALUES(%s, %s, %s, %s, %s);'
		sql2 = 'INSERT IGNORE INTO classroom (building, room_no, capacity) VALUES(%s, %s, %s);'
		n = amount
		for row in view:
			if n < 0:
				self.cnx.commit()
				return
			if row[2] != building:
				room_no = 0
				building = row[2]
			for _ in range(random.choice(range(6))):
				data = (row[0], semester, year, building, room_no)
				room_no += 1
				data2 = (building, room_no, random.choice(range(6, 11)) * 10)
				self.cursor.execute(sql, data)
				self.cursor.execute(sql2, data2)
			n -= 1

	def teaches(self):
		self.cursor.execute('SELECT dept_name FROM department;')
		for dept in self.cursor.fetchall():
			self.cursor.execute('SELECT ID FROM instructor WHERE dept_name = \"' + dept[0] + '\";')
			teachers = self.cursor.fetchall()
			teachNums = len(teachers)
			teachSelect = 0
			self.cursor.execute('SELECT course_id FROM course WHERE dept_name = \"' + dept[0] + '\";')
			for course in self.cursor.fetchall():
				self.cursor.execute('SELECT class_id FROM class WHERE course_id = \"' + str(course[0]) + '\";')
				for class_ in self.cursor.fetchall():
					sql = 'INSERT IGNORE INTO teaches (ID, course_id, class_id) VALUES (%s, %s, %s);'
					data = (str(teachers[teachSelect % teachNums][0]), str(course[0]), str(class_[0])) 
					self.cursor.execute(sql, data)
					teachSelect += 1
		self.cnx.commit()

	def takes(self):
		self.cursor.execute('SELECT dept_name FROM department;')
		for dept in self.cursor.fetchall():
			self.cursor.execute('SELECT course.course_id, class.class_id, class.building, class.room_no FROM course JOIN class ON course.course_id = class.course_id WHERE course.dept_name LIKE \"' + dept[0]+ '\";')
			classes =  self.cursor.fetchall()
			self.cursor.execute('SELECT ID FROM student WHERE dept_name = \"' + dept[0] + '\";')
			for student in self.cursor.fetchall():
				sql = 'INSERT IGNORE INTO takes (ID, course_id, class_id) VALUES (%s, %s, %s);'
				#sql2 = 'UPDATE classroom SET used =used + 1 WHERE building = %s AND room_no = %s;'
				for _ in range(random.choice(range(6))):
					try:
						choice = random.choice(classes)
					except:
						continue
					data = (str(student[0]), str(choice[0]), str(choice[1]))
					self.cursor.execute(sql, data)
			self.cnx.commit()

	def close(self):
		self.cursor.close()
		self.cnx.close()


if __name__ == '__main__':
	filler = Filler()
	#filler.fillFemales(50000)
	#filler.fillMales(50000)
	#filler.fillFemalesT(5000)
	#filler.fillMalesT(5000)
	filler.class_()
	filler.teaches()
	filler.takes()
	filler.close()

