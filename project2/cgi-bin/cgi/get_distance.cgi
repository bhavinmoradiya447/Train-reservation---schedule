#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
my $db=new Database();
my $cgi=new CGI();

my $source=$cgi->param("source");
my $dest=$cgi->param("dest");
my $tr_no=$cgi->param("tr_no");

      my $result=$db->select_query("select t1.distance,t2.distance from train_time t1,train_time t2 where t1.station_code='".$source."' and t2.station_code='".$dest."' and t1.tr_no=$tr_no and t2.tr_no=$tr_no");
     foreach(@$result)
     {
                
                my $distance=$_->[1] - $_->[0];
                if($distance > 0)
                {print "Content-type:text/html\n\r\n\r";
                  print "1"; 
                 }
                else
                {
                  print "Content-type:text/html\n\r\n\r";
                  print "0"; 
                 }
     }   
               
