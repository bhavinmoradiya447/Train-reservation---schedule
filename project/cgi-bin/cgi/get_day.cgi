#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
my $db=new Database();
my $cgi=new CGI();

my $source=$cgi->param("tr_source");
my $tr_no=$cgi->param("tr_no");

      my $result=$db->select_query("select day from train_time where station_code='".$source."' and tr_no=$tr_no")->[0][0];
                  my $day=join ";",@$result;
                  print "Content-type:text/html\n\r\n\r";
                  
                  print $day; 
               
