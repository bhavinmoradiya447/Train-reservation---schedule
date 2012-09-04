#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
my $db=new Database();
my $cgi=new CGI();

my ($userid,$phone,$email,$password,$name,$oldpassword)=($cgi->param("userid"),$cgi->param("ph_no"),$cgi->param("email"),$cgi->param("password"),$cgi->param("name"),$cgi->param("oldpassword"));

my $result=$db->select_query("SELECT \"password\",\"name\",\"ph_no\",\"email\" FROM \"public\".\"user\" WHERE \"user_id\" = '"."$userid"."'")->[0];

$name=$name eq "" ? $result->[1]:$name;

# if($name eq "")
# { $name=$result->[1];}

$phone=$phone eq "" ? $result->[2]:$phone;

$email=$email eq "" ? $result->[3]:$email;

$password=$password eq "" ? $result->[0]:$password;
my $pwd=$result->[0];


$db->update_query("update \"user\" set name='".$name."',ph_no=$phone,email='".$email."',password='".$password."' where user_id='".$userid."'");

   $result=$db->select_query("SELECT \"password\",\"name\",\"ph_no\",\"email\" FROM \"public\".\"user\" WHERE \"user_id\" = '".$userid."'")->[0];
   print "Content-type:text/html\n\r\n\r";
   if(defined($oldpassword))
   {
         if($oldpassword eq $pwd)
         {
         print "$result->[1];$result->[2];$result->[3];true";         
         }
         else
         {
            print "$result->[1];$result->[2];$result->[3];false";   
         }
   }
   else
   {
         print "$result->[1];$result->[2];$result->[3];false";   
   }
   