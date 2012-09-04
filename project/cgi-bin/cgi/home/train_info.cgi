#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
use CGI;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
my $db=new Database();
my $cgi=new CGI();

my ($tr_no,$tr_name,$class,$quota)=($cgi->param("tr_no_drop_down"),$cgi->param("tr_name_drop_down"),$cgi->param("tr_class_drop_down"),$cgi->param("tr_quota_drop_down"));

my $template=new HTML::Template(filename=>'../../html/home/train_info.tmpl'); 

if(($tr_no ne "") or ($tr_no eq "" and $tr_name ne "")or( $tr_name ne "" and $tr_no ne ""))
{
    if($tr_name ne "" and $tr_no eq "")
    {
      my $tr_no_arr_ref=$db->select_query("select * from train where tr_name='".$tr_name."'");
                         my @arr;
                        foreach my $no  (@$tr_no_arr_ref)  
                        {
                        #display train info
                         $tr_no=$no->[0];
                        my $result=$db->select_query("select * from train where tr_no=$no->[0]");
                                    foreach(@$result)
                                    {
                                    my $day=$db->select_query("select day from train_time where tr_no=$_->[0]");
                                    push @arr,{TRAIN_NO=>$_->[0],TRAIN_NAME=>$_->[1],SOURCE=>$_->[2],DESTINATION=>$_->[3],DAY=>@{$day->[0][0]}};
                                    }
                        }             
                       
    $template->param(TRAIN_INFO=>\@arr);
    }
  
    elsif($tr_no ne "" ){
                                                #display train info
                                     my $result=$db->select_query("select * from train where tr_no=$tr_no");
                                     my @arr;
                                    foreach(@$result)
                                    {
                                                my $day=$db->select_query("select day from train_time where tr_no=$_->[0]");
                                                push @arr,{TRAIN_NO=>$_->[0],TRAIN_NAME=>$_->[1],SOURCE=>$_->[2],DESTINATION=>$_->[3],DAY=>@{$day->[0][0]}};
                                    }
                                    $template->param(TRAIN_INFO=>\@arr);
    }
  
    if($class ne "" and $quota ne "") #display seat info
    {
            #select from class and quota
             my $result=$db->select_query("select * from train_seat where tr_no=$tr_no and quota='".$quota."'  and class='".$class."'");
                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$_->[0],CLASS=>$_->[1],QUOTA=>$_->[2],SEAT=>$_->[3]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     elsif($class ne "" and $quota eq "")
     {
        #select from class
                  my $result=$db->select_query("select * from train_seat where tr_no=$tr_no and class='".$class."'");
                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$_->[0],CLASS=>$_->[1],QUOTA=>$_->[2],SEAT=>$_->[3]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     elsif($class eq "" and $quota ne "")
     {
        #select from quota
                  my $result=$db->select_query("select * from train_seat where tr_no=$tr_no and quota='".$quota."'");
                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$_->[0],CLASS=>$_->[1],QUOTA=>$_->[2],SEAT=>$_->[3]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     else
     {
                  my $result=$db->select_query("select * from train_seat where tr_no=$tr_no");
                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$_->[0],CLASS=>$_->[1],QUOTA=>$_->[2],SEAT=>$_->[3]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     
}




print "Content-type:text/html\n\r\n\r";

print $template->output;
