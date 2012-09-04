#!/usr/bin/perl -w
use strict;
use warnings;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
my $db=new Database();
my $cgi=new CGI();

my $reservation_no=$cgi->param("reservation_no");
my $result=$db->select_query("select * from reservation where reservation_no=$reservation_no");
print "Content-type:text/html\n\r\n\r";
print "$result->[0][0];$result->[0][1];$result->[0][2];$result->[0][3];$result->[0][4];$result->[0][5];$result->[0][6];".$db->select_query("select station_name from station where station_code='".$result->[0][7]."'")->[0][0].";".$db->select_query("select station_name from station where station_code='".$result->[0][8]."'")->[0][0].";$result->[0][9];$result->[0][7];$result->[0][8]";
