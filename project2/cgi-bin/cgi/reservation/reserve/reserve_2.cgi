#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
my $db=new Database();
my $cgi=new CGI();
my ($distance,$concession,$basic_fare,$total,$price);
my $is_super_fast="false";
my $return_value;
my($tr_no,$source,$dest,$class,$day,$month,$year,$quota)=($cgi->param("tr_no"),$cgi->param("tr_source"),$cgi->param("tr_dest"),$cgi->param("tr_class"),$cgi->param("lccp_day"),$cgi->param("lccp_month"),$cgi->param("lccp_year"),$cgi->param("tr_quota"));
my $date="$year-$month-$day";

sub tr_name{
                my $result=$db->select_query("select tr_name from train where tr_no=$tr_no");
                my $data=[];
                foreach(@$result)
                {
                        return $_->[0];
                 }
             
 }
 
 sub tr_type{
                 my $name=&tr_name;
                 if($name=~/Super Fast/i)
                 {$is_super_fast="true";
                  return "Super Fast";}
                 elsif($name=~/Intercity/i)
                 {return "Intercity";}
                 elsif($name=~/Rajdhani/i)
                 {return "Rajdhani";}
                 elsif($name=~/Garib Rath/i)
                 {return "Garib Rath";}
                 elsif($name=~/Shatabdi/i)
                 {return "Shatabdi";}
                elsif($name=~/Mail/i)
                 {return "Mail Express";}
                 elsif($name=~/Kranti/i)
                 {return "Krainti";}
                 else
                 {return "Express";}
}

sub distance{
      my $result=$db->select_query("select t1.distance,t2.distance from train_time t1,train_time t2 where t1.station_code='".$source."' and t2.station_code='".$dest."' and t1.tr_no=$tr_no and t2.tr_no=$tr_no");
     foreach(@$result)
     {
                
$distance=$_->[1] - $_->[0];
                if($distance > 0)
                {return $distance;}
     }   
               
}

sub fare{
      my $result=$db->select_query("select price from price where tr_no=$tr_no and class='".$class."'");
     foreach(@$result)
     {
                $price=$_->[0];
                $total=$price*$distance;
                return $total;
     }   
 
}




my $flag=$db->select_query('select count(*) from price where \''.$date.'\'=current_date and (SELECT to_timestamp(t1,\'HH24:MI\')-to_timestamp(t2,\'HH24:MI\')
from 
(select dep_time as t1 from train_time where tr_no='.$tr_no.' and station_code=\''.$source.'\') as tt1,(SELECT to_char(now()::time,\'hh24:mi\') as t2)as tt2
)<interval \'0:0\'')->[0][0];

if($flag+0>0)
{
 print "Content-type:text/html\n\r\n\r";

 print "time over"
}
else
{
$return_value.="tr_no=$tr_no;";
$return_value.="tr_nane=".&tr_name.";";
$return_value.="date=$date;";
$return_value.="source=".$db->select_query("select station_name from station where station_code='".$source."'")->[0][0].";"; # to set  train  source
$return_value.="dest=".$db->select_query("select station_name from station where station_code='".$dest."'")->[0][0].";"; # to set  train  source
$return_value.="type=".&tr_type.";";
$return_value.="distance=".&distance.";";
$return_value.="class=$class;";
$return_value.="fare=".&fare.";";
if($is_super_fast eq "true")
{
$return_value.="super_carge=30;";
}
else
{
$return_value.="super_carge=0;";
}

my $count=$db->select_query("select count(*) from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
     if($count+0==0){
                                  my $seat_info=$db->select_query("select seat from train_seat where tr_no=$tr_no and class='".$class."' and  quota='".$quota."'")->[0][0];
                                 $db->insert_query("waiting",$date,$tr_no,$class,$quota,$source,$dest,$seat_info,0);
                             }
            my $result=$db->select_query("select seat_remain,waiting from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");

                 if($result->[0][0]+0>0)
                {
                   $return_value.="Available=$result->[0][0];"
                }
                else
                {
                     $return_value.="Waiting=$result->[0][1];"
                }
print "Content-type:text/html\n\r\n\r";
print $return_value;

}