# -*- encoding=utf8 -*-

'''
open .cn config file
.cn file is a kind of file for config or complex text content storage with time record.
this will help you to record the config file's every change time and what be changed,
this is very usefull for administrator.
you can store only one json or dict which start with { and end with }.
If a .cn file is empty,it means {}

{
    "a":1,
    "c":[1,2],
    "b":{
        "a":3,
        "e":{
            "b":4
        }
    }
}

in .cn file it will be like this:

+@:a:1,2022-07-01 12:13:11.10001
+@:c:1,2022-07-01 12:13:11.10040
+@:c:2,2022-07-01 12:13:11.20000
+@:b:a:3, 2022-07-01 12:13:11.20000
+@:b:e:b:4, 2022-07-01 12:13:11.20000

if you want to delete the "e" branch you can add this reccord to the .cn file
-@:b:e:b:4, 2022-07-01 12:13:11.30000



[1,2,3,4]

+(0,0)@:1, 2022-07-01 12:13:11.30000
+(0,1)@:2, 2022-07-01 12:13:11.30000
+(0,2)@:3, 2022-07-01 12:13:11.30000
+(0,3)@:4, 2022-07-01 12:13:11.30000

{
    a:[1,2,3,4]
}

+(0,0)(0,0)@:a:1,2022-07-01 12:13:11.30000
+(0,0)(0,1)@:a:2,2022-07-01 12:13:11.30000
+(0,0)(0,2)@:a:3,2022-07-01 12:13:11.30000
+(0,0)(0,3)@:a:4,2022-07-01 12:13:11.30000

This is the graph database's log and config design.It is very elegant and awesome.

'''

class cnlogconf():
    pass