#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
use CGI;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
my $db=new Database();
my $cgi=new CGI();

my ($tr_no,$class,$quota,$date,$source,$dest)=($cgi->param("tr_no_drop_down"),$cgi->param("tr_class_drop_down"),$cgi->param("tr_quota_drop_down"),$cgi->param("year")."-".$cgi->param("month")."-".$cgi->param("day"),$cgi->param("tr_source_drop_down"),$cgi->param("tr_dest_drop_down"));

my $template=new HTML::Template(filename=>'../../html/home/waiting_list.tmpl'); 

  
if($tr_no ne "" )
{
        #display train info
        my $result=$db->select_query("select * from train where tr_no=$tr_no");
        my @arr;
        foreach(@$result)
        {
            my $day=$db->select_query("select day from train_time where tr_no=$_->[0]");
            push @arr,{TRAIN_NO=>$_->[0],TRAIN_NAME=>$_->[1],SOURCE=>$source,DESTINATION=>$dest,DATE=>$date};
        }
        $template->param(TRAIN_INFO=>\@arr);
    }
  
my $count=$db->select_query("select count(*) from waiting where date='".$date."' and tr_no=$tr_no and and source='".$source."' and dest='".$dest."'")->[0][0];
         if($count+0==0)
            {
             my $seat_info=$db->select_query("select * from train_seat where tr_no=$tr_no");
             foreach my $res(@$seat_info){
                $db->insert_query("waiting",$date,$tr_no,$res->[1],$res->[2],$source,$dest,$res->[3],0);
              }
            }



    if($class ne "" and $quota ne "") #display seat info
    {
            my $result=$db->select_query("select * from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");

                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$tr_no,CLASS=>$_->[2],QUOTA=>$_->[3],SEAT=>$_->[6],WAITING=>$_->[7]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     
     elsif($class ne "" and $quota eq "")
     {
        #select from class
            my $result=$db->select_query("select * from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."'  and source='".$source."' and dest='".$dest."'");

                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$tr_no,CLASS=>$_->[2],QUOTA=>$_->[3],SEAT=>$_->[6],WAITING=>$_->[7]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     elsif($class eq "" and $quota ne "")
     {
        #select from quota
            my $result=$db->select_query("select * from waiting where date='".$date."' and tr_no=$tr_no and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");

                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$tr_no,CLASS=>$_->[2],QUOTA=>$_->[3],SEAT=>$_->[6],WAITING=>$_->[7]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     else
     {
            my $result=$db->select_query("select * from waiting where date='".$date."' and tr_no=$tr_no and source='".$source."' and dest='".$dest."'");

                  my $arr=[];
                  foreach(@$result)
                  {
                          push @$arr,{TRAIN_NO=>$tr_no,CLASS=>$_->[2],QUOTA=>$_->[3],SEAT=>$_->[6],WAITING=>$_->[7]};          
                  }
                  $template->param(TRAIN_SEAT_INFO=>$arr);
     }
     





# # sub tr_no{
# my $result=$db->get_train_no();
# my $data=[];
# foreach(@$result)
# {
# push @$data,{TR_NO=>$_};
# #=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
# }
# return $data;
# }

# # sub tr_name{
# my $result=$db->get_train_name();
# my $data=[];
# foreach(@$result)
# {
# push @$data,{TR_NAME=>$_};
# #=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
# }
# return $data;
# }

# $template->param(TRAIN_NO=>&tr_no); # to set  train  number
# $template->param(TRAIN_NAME=>&tr_name); # to set  train  name

print "Content-type:text/html\n\r\n\r";

print $template->output;
