#!/usr/bin/perl -w
use strict;
use warnings;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI;
my $db=new Database();
my $cgi=new CGI();
my $return_value="";
my $reservation_no=$cgi->param("reservation_no");
my $user_id=$cgi->param("user_id");

 my $count=$db->select_query("select count(*) from reservation where reservation_no=$reservation_no")->[0][0];
if($count+0 >0)
{
    my $result=$db->select_query("select * from reservation where reservation_no=$reservation_no");
    if($result->[0][1] eq $user_id)
    {
        $return_value.=$result->[0][0].";";
        $return_value.=$result->[0][5].";";
        $return_value.=$db->select_query("SELECT \"name\" FROM \"public\".\"user\" WHERE \"user_id\" = '".$result->[0][1]."'")->[0][0].";";
        $return_value.=$result->[0][2].";";
        $return_value.=$db->select_query("select station_name from station where station_code='".$result->[0][7]."'")->[0][0].";";
        $return_value.=$db->select_query("select station_name from station where station_code='".$result->[0][8]."'")->[0][0].";";
        $return_value.=$result->[0][3].";";
        $return_value.=$result->[0][4].";";
        my $arr=join ",",@{$result->[0][12]};
        $return_value.=$arr.";";
        $return_value.=$result->[0][14].";";
        my $distance=$db->select_query("select t1.distance,t2.distance from train_time t1,train_time t2 where t1.station_code='".$result->[0][7]."' and t2.station_code='".$result->[0][8]."' and t1.tr_no=$result->[0][2] and t2.tr_no=$result->[0][2]");
        foreach(@$distance)
        {
                
                my $dist=$_->[1] - $_->[0];
                if($dist > 0)
                {$return_value.=$dist.";";}
        }
    }
    else
    {
           $return_value.="invalid user";
    }
}
else
{
          $return_value.="invalid reservation number";
   
}

print "Content-type:text/html\n\r\n\r";
print $return_value;
#print "$result->[0][0];$result->[0][1];$result->[0][2];$result->[0][3];$result->[0][4];$result->[0][5];$result->[0][6];".$db->select_query("select station_name from station where station_code='".$result->[0][7]."'")->[0][0].";".$db->select_query("select station_name from station where station_code='".$result->[0][8]."'")->[0][0].";$result->[0][9];$result->[0][7];$result->[0][8]";
