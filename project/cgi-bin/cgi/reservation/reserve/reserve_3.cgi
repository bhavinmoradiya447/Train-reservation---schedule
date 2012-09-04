#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use SMS;
use CGI;
my $db=new Database();
my $cgi=new CGI();
my @seat_allow;
my $no_of_seat_allow=0;
my $no_of_seat_remain=0;

#my ($distance,$concession,$basic_fare,$total,$price);
my $is_super_fast="false";
my $return_value;
my($tr_no,$source,$dest,$class,$day,$month,$year,$quota,$no_of_seat,$concession,$price,$user_id)=($cgi->param("tr_no"),$cgi->param("tr_source"),$cgi->param("tr_dest"),$cgi->param("tr_class"),$cgi->param("lccp_day"),$cgi->param("lccp_month"),$cgi->param("lccp_year"),$cgi->param("tr_quota"),$cgi->param("no_of_seat"),$cgi->param("concession"),$cgi->param("total"),$cgi->param("user_id"));
my $date="$year-$month-$day";
$no_of_seat=$no_of_seat+0;

my $total_seat=$no_of_seat;

my $count=$db->select_query("select count(*) from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
           if($count+0==1)
           {
                      my $seat=$db->select_query("select no_of_seat from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                      if($no_of_seat <=$seat+0)
                      {       
                                 $seat=$seat-$no_of_seat;
                                my  $queue=$db->select_query("select queue from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                                for(my $i=0;$i<$no_of_seat;$i++)
                                {
                                     push @seat_allow,shift @$queue;
                                     $no_of_seat_allow++;
                                }  
                                $no_of_seat=0;
                              my $arr=join ",",@$queue;  
                             $db->update_query("update available_cancel set no_of_seat=$seat,queue='{".$arr."}' where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");  
                      }                     
                      else
                      {
                                $no_of_seat_remain=$no_of_seat-$seat;  
                               my  $queue=$db->select_query("select queue from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                                for(my $i=0;$i<$seat+0;$i++)
                                {
                                     push @seat_allow,shift @$queue;
                                     $no_of_seat_allow++;
                                }  
                             $db->update_query("delete from available_cancel  where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");  
                                $no_of_seat=$no_of_seat_remain;  
                      }          
           }


my $seat=$db->select_query("select seat_remain from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
if($seat+0>0 and $seat+0>= $no_of_seat)
{
                                my $orignal_seat=$db->select_query("select seat from train_seat where tr_no=$tr_no and class='".$class."' and  quota='".$quota."'")->[0][0];
                                my $seat_assign=$orignal_seat-$seat;
                                $seat=$seat-$no_of_seat;
                                for(my $i=0;$i<$no_of_seat;$i++)
                                {
                                     push @seat_allow,++$seat_assign;
                                     $no_of_seat_allow++;
                                }  
                                $no_of_seat=0;
                             $db->update_query("update waiting set seat_remain=$seat where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");  
}
elsif($seat+0>0 and $seat+0< $no_of_seat)
{
                               my $waiting=$db->select_query("select waiting from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                                my $orignal_seat=$db->select_query("select seat from train_seat where tr_no=$tr_no and class='".$class."' and  quota='".$quota."'")->[0][0];
                                my $seat_assign=$orignal_seat-$seat;
                                for(my $i=0;$i<$seat;$i++)
                                {
                                     push @seat_allow,++$seat_assign;
                                     $no_of_seat_allow++;
                                }  
                                $no_of_seat=$no_of_seat-$seat;
                                $seat=0;
                                $waiting+=$no_of_seat;
                                $db->update_query("update waiting set seat_remain=$seat,waiting=$waiting  where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");  
                                $no_of_seat=0;
}
elsif($seat+0==0)
{
                               my $waiting=$db->select_query("select waiting from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                                $waiting+=$no_of_seat;
                                $db->update_query("update waiting set seat_remain=$seat,waiting=$waiting  where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");  
                                $no_of_seat=0;
}

if($no_of_seat==0)
{
   my @pnr=localtime();
my $reservation_no=join "",@pnr;
if(length($reservation_no)>16 )
{
    $reservation_no=substr $reservation_no,0,16;
}
elsif(length($reservation_no)<16)
{
$reservation_no=$reservation_no+1000000000000000;    
}

     my $seat_number=join ",",@seat_allow;
     my $time=$db->select_query("SELECT CURRENT_TIME")->[0][0];
     $db->insert_query("reservation",$reservation_no,$user_id,$tr_no,$class,$quota,$date,$concession,$source,$dest,$total_seat,$no_of_seat_allow,$total_seat-$no_of_seat_allow,"{$seat_number}",$time,$price);
     
     $db->insert_query("transaction",$reservation_no,$user_id,$price);

     my $user=$db->select_query("select ph_no,email from \"user\" where user_id='".$user_id."'")->[0];
     my $sms=new SMS();
     $sms->send_mail_sms($user->[0],$user->[1],$reservation_no,$seat_number);

print "Content-type:text/html\n\r\n\r";
print "$reservation_no;$seat_number;".($total_seat-$no_of_seat_allow);     

}

































# sub tr_name{
                # my $result=$db->select_query("select tr_name from train where tr_no=$tr_no");
                # my $data=[];
                # foreach(@$result)
                # {
                        # return $_->[0];
                 # }
             
# #  }
 
# #  sub tr_type{
                 # my $name=&tr_name;
                 # if($name=~/Super Fast/i)
                 # {$is_super_fast="true";
                  # return "Super Fast";}
                 # elsif($name=~/Intercity/i)
                 # {return "Intercity";}
                 # elsif($name=~/Rajdhani/i)
                 # {return "Rajdhani";}
                 # elsif($name=~/Garib Rath/i)
                 # {return "Garib Rath";}
                 # elsif($name=~/Shatabdi/i)
                 # {return "Shatabdi";}
                # elsif($name=~/Mail/i)
                 # {return "Mail Express";}
                 # elsif($name=~/Kranti/i)
                 # {return "Krainti";}
                 # else
                 # {return "Express";}
# }

# # sub distance{
      # my $result=$db->select_query("select t1.distance,t2.distance from train_time t1,train_time t2 where t1.station_code='".$source."' and t2.station_code='".$dest."' and t1.tr_no=$tr_no and t2.tr_no=$tr_no");
     # foreach(@$result)
     # {
                
# # $distance=$_->[1] - $_->[0];
                # if($distance > 0)
                # {return $distance;}
     # }   
               
# # }

# # sub fare{
      # my $result=$db->select_query("select price from price where tr_no=$tr_no and class='".$class."'");
     # foreach(@$result)
     # {
                # $price=$_->[0];
                # $total=$price*$distance;
                # return $total;
     # }   
 
# # }

# # $return_value.="tr_no=$tr_no;";
# $return_value.="tr_nane=".&tr_name.";";
# $return_value.="date=$date;";
# $return_value.="source=".$db->select_query("select station_name from station where station_code='".$source."'")->[0][0].";"; # to set  train  source
# $return_value.="dest=".$db->select_query("select station_name from station where station_code='".$dest."'")->[0][0].";"; # to set  train  source
# $return_value.="type=".&tr_type.";";
# $return_value.="distance=".&distance.";";
# $return_value.="class=$class;";
# $return_value.="fare=".&fare.";";
# if($is_super_fast eq "true")
# {
# $return_value.="super_carge=30;";
# }
# else
# {
# $return_value.="super_carge=0;";
# }

# # 
# my $count=$db->select_query("select count(*) from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
     # if($count+0==0){
                                  # my $seat_info=$db->select_query("select seat from train_seat where tr_no=$tr_no and class='".$class."' and  quota='".$quota."'")->[0][0];
                                 # $db->insert_query("waiting",$date,$tr_no,$class,$quota,$source,$dest,$seat_info,0);
                             # }
            # my $result=$db->select_query("select seat_remain,waiting from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");

# #                  if($result->[0][0]+0>0)
                # {
                   # $return_value.="Available=$result->[0][0];"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
                # }
                # else
                # {
                     # $return_value.="Waiting=$result->[0][1];"
                # }
# print "Content-type:text/html\n\r\n\r";
# print $return_value;

# 
