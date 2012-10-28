Expyred
---------------

Source code to [http://expyred.kat.sh], which is an online regular expression editor/tester.

I made this years ago..2007 or 2008, and haven't exactly touched it since then.  
There are room for improvements :)

**Created with:**  
[web.py] as the framework  
[mako] for the templating


**Set up the mysql database with:** 

> create database expyred;  
> use expyred;  
> create table permalinks (   
> linkID int not null auto_increment,  
> primary key (linkID),  
> regex varchar(255),  
> varchar(255),  
> options varchar(20), date datetime);  



[http://expyred.kat.sh]:http://expyred.kat.sh
[web.py]:http://webpy.org/
[mako]:http://www.makotemplates.org/
