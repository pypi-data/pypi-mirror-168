#!/usr/bin/python3
# -*- coding: utf8 -*-


#约定0为生产，1为预生产，2为测试

apiserver=[
	{	#生产环境
		"up":"http://sw3.rt/swapi/updateProgram",
		"down":"http://sw3.rt/swapi/programInfo",
	},
	{	#预生产环境
		"up":"http://sw3.rt/swapi/updateProgram",
		"down":"http://sw3.rt/swapi/programInfo",
	},
	{	#测试环境
		"up":"http://sw3.test/swapi/updateProgram",
		"down":"http://sw3.test/swapi/programInfo",
	},
	
]

defenvprefix="sw3"
