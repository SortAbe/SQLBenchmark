#!/bin/env python3
#Abrahan Diaz
#Version 0.8


import random
import re
import time
import mysql.connector

class Filler:
	cnx = mysql.connector.connect(
		host='localhost',
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
			data = (self.femaleNames[i%flen], self.lastNames[i%llen], True, self.departmentList[i%dlen] , credit)
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
			data = (self.femaleNames[i%flen], self.lastNames[i%llen], True, self.departmentList[i%dlen])
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
			data = (self.maleNames[i%mlen], self.lastNames[i%llen], False, self.departmentList[i%dlen] , credit)
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
			data = (self.maleNames[i%mlen], self.lastNames[i%llen], False, self.departmentList[i%dlen])
			self.cursor.execute(sql, data)
		self.cnx.commit()

	def class_(self, year=2023, semester='Spring'):
		self.cursor.execute('SELECT COUNT(*) FROM instructor;')
		amount = self.cursor.fetchall() * 3
		self.cursor.execute('SELECT course.course_id, course.dept_name, department.building  FROM course JOIN department ON course.dept_name = department.dept_name ORDER BY department.building;')
		view = self.cursor.fetchall()
		building = None
		room_no = 0
		sql = 'INSERT INTO class (course_id, semester, year, building, room_no) VALUES(%s, %s, %s, %s, %s)'
		sql2 = 'INSERT INTO classroom (building, room_no, capacity) VALUES(%s, %s, %s)'
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

	def close(self):
		self.cursor.close()
		self.cnx.close()


if __name__ == '__main__':
	filler = Filler()
	#filler.fillFemales()
	#filler.fillMales()
	#filler.fillFemalesT()
	#filler.fillMalesT()
	filler.class_()
	filler.close()

