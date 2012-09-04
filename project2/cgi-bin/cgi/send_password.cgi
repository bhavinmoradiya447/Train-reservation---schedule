#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
use SMS;
my $db=new Database();
my $cgi=new CGI();
my $sms=new SMS();

my $user_id=$cgi->param("userid");
       
       if($db->user_validation($user_id)=~/true/)
       {     
            my $result=$db->select_query("select password,ph_no,email from \"user\" where user_id='".$user_id."'")->[0];
            $sms->send_password($result->[1],$result->[2],$result->[0]); 
            print "Content-type:text/html\n\r\n\r";
            print "1";     
      }       
       else
       {
            print "Content-type:text/html\n\r\n\r";
            print "0";     
      }
         
