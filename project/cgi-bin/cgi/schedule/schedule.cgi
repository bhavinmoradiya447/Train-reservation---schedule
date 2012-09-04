#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
use CGI;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
my $db=new Database();
my $cgi=new CGI();
my $button=$cgi->param("button");

sub tr_source{
        my $result=$db->get_station_name();
        my $data=[];
        foreach(@$result)
        {
            push @$data,{TR_SOURCE=>$_->[0],TR_SOURCE_CODE=>$_->[1]};
            #=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
        }
        return $data;
}
sub tr_dest{
        my $result=$db->get_station_name();
        my $data=[];
        foreach(@$result)
        {
            push @$data,{TR_DEST=>$_->[0],TR_DEST_CODE=>$_->[1]};
            #=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
        }
        return $data;
}


my $template=new HTML::Template(filename=>'../../html/schedule/schedule.tmpl'); 
#$template->param(TRAIN_NO=>&tr_no); # to set  train  number
$template->param(TRAIN_SOURCE=>&tr_source); # to set  train  source
$template->param(TRAIN_DEST=>&tr_dest); # to set  train  destination

if($button eq "Submit")
{
    
     my ($source,$dest)=($cgi->param("tr_source_drop_down"),$cgi->param("tr_dest_drop_down"));
     my $result=$db->select_query("select t1.* ,t2.distance from train_time t1,train_time t2 where t1.station_code='".$source."' and t2.station_code='".$dest."' and t1.tr_no=t2.tr_no");
     my $arr=[];
     foreach(@$result)
     {
        if($_->[2]<$_->[7])
        {

       my $tr_name=$db->select_query("select tr_name from train where tr_no=$_->[0]");
       push @$arr,{TRAIN_NO=>$_->[0],TRAIN_NAME=>$tr_name->[0][0]};  
         
         }
     }   
        
   $template->param(STATION_SCHEDULE=>$arr);     
}
elsif($button eq "Get Train Schedule")
{   
    my $tr_no=$cgi->param("tr_no");
    my $result=$db->select_query("select * from train_time where tr_no=$tr_no");
     my $arr=[];
     foreach(@$result)
     {
          my $tr_name=$db->select_query("select station_name from station where station_code='".$_->[1]."'")->[0][0];
          my $day=join ",",@{$_->[5]};
          push @$arr,{TRAIN_NO => $_->[0], ST_CODE => $tr_name, DISTANCE => $_->[2], ARR_TIME => $_->[3], DEP_TIME => $_->[4], DAY => $day, STATE => $_->[6]};  
     }   
        
   $template->param(TRAIN_SCHEDULE=>$arr);     
}


print "Content-type:text/html\n\r\n\r";
print $template->output;
