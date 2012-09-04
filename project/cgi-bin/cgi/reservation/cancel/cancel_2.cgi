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
my ($price);
my($tr_no,$source,$dest,$class,$date,$reservation_no,$no_of_seat_cancel,$quota)=($cgi->param("tr_no"),$cgi->param("tr_source"),$cgi->param("tr_dest"),$cgi->param("tr_class"),$cgi->param("date"),$cgi->param("reservation_no"),$cgi->param("no_of_seat_cancel"),$cgi->param("tr_quota"));
my $orignal_no_of_seat_cancel=$no_of_seat_cancel+0;
$no_of_seat_cancel+=0;


sub distance{
      my $result=$db->select_query("select t1.distance,t2.distance from train_time t1,train_time t2 where t1.station_code='".$source."' and t2.station_code='".$dest."' and t1.tr_no=$tr_no and t2.tr_no=$tr_no");
     foreach(@$result)
     {
                
                my $distance=$_->[1] - $_->[0];
                if($distance > 0)
                {return $distance;}
     }   
               
}

#SELECT to_char(now()::time,'hh24:mi')
my $flag=$db->select_query(' select count(*) from reservation where reservation_no='.$reservation_no.' and ((date<current_date) or((date=current_date) and (SELECT to_timestamp(t1,\'HH24:MI\')-to_timestamp(t2,\'HH24:MI\')
from 
(select dep_time as t1 from train_time where tr_no='.$tr_no.' and station_code=\''.$source.'\') as tt1,(SELECT to_char(now()::time,\'hh24:mi\') as t2)as tt2
)<interval \'0:0\'))')->[0][0];

if($flag+0>0)
{
 print "Content-type:text/html\n\r\n\r";

 print "time over"
}

else{
      my $result=$db->select_query("select price from price where tr_no=$tr_no and class='".$class."'");
     foreach(@$result)
     {
                $price=$_->[0];
                $price=$price * &distance;
     }   
 

my $waiting=$db->select_query("select waiting from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0] +0;
           if($waiting+0>0)
           {
                       my $cancel_user=$db->select_query("select * from reservation where reservation_no=$reservation_no");
                       if($no_of_seat_cancel<=$cancel_user->[0][11]+0)
                       {
                                  $cancel_user->[0][9]=$cancel_user->[0][9]-$no_of_seat_cancel;
                                  $cancel_user->[0][11]=$cancel_user->[0][11] - $no_of_seat_cancel;
                                  $cancel_user->[0][14]=$cancel_user->[0][14] - ($price*$no_of_seat_cancel);
                                  $db->update_query("update reservation set no_of_seat=$cancel_user->[0][9],no_seat_remain=$cancel_user->[0][11],amount=$cancel_user->[0][14]  where reservation_no=$reservation_no");
                                  
                                  $waiting=$waiting-$no_of_seat_cancel;
                                  $db->update_query("update waiting set waiting=$waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                  $no_of_seat_cancel=0;
                                  
                                             
                       
                       }
                       else
                       {
                                  $waiting=$waiting-$cancel_user->[0][11];
                                  $db->update_query("update waiting set waiting=$waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                  
                                  $cancel_user->[0][9]=$cancel_user->[0][9]-$cancel_user->[0][11];
                                  $no_of_seat_cancel=$no_of_seat_cancel-$cancel_user->[0][11];
                                  $cancel_user->[0][14]=$cancel_user->[0][14] - ($price*$cancel_user->[0][11]);
                                  $cancel_user->[0][11]=0;
                                  $db->update_query("update reservation set no_of_seat=$cancel_user->[0][9],no_seat_remain=$cancel_user->[0][11],amount=$cancel_user->[0][14]  where reservation_no=$reservation_no");
                                  
                                  if($waiting>0)
                                  {
                                          my $cancel_user=$db->select_query("select * from reservation where reservation_no=$reservation_no");   
                                          my   $reserve_wait=$db->select_query("select * from reservation where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                          foreach my $row (@$reserve_wait)
                                          {         
                                                     if($no_of_seat_cancel==0){last;}

                                                     if($row->[11]+0>0)
                                                     {
                                                               if($no_of_seat_cancel>=$row->[11]+0)
                                                               {
                                                                           $no_of_seat_cancel=$no_of_seat_cancel-$row->[11];
                                                                           my $arr_cancel=$cancel_user->[0][12];
                                                                           my $arr_reserve=$row->[12];
                                                                           for(my $i=0;$i<$row->[11]+0;$i++)
                                                                           {
                                                                                      push @$arr_reserve,pop @$arr_cancel;
                                                                           }
                                                                           
                                                                           
                                                                           $waiting=$waiting-$row->[11];
                                                                           $db->update_query("update waiting set waiting=$waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                    
                                                                            my $arr_string= join ",",@$arr_cancel;
                                                                            $cancel_user->[0][9]=$cancel_user->[0][9]-$row->[11];
                                                                            $cancel_user->[0][10]=$cancel_user->[0][10]-$row->[11];
                                                                            $cancel_user->[0][14]=$cancel_user->[0][14]-($price*$row->[11]);
                                                                            $db->update_query("update reservation set no_of_seat=$cancel_user->[0][9],no_seat_assign=$cancel_user->[0][10],seat_number='{".$arr_string."}',amount=$cancel_user->[0][14]  where reservation_no=$reservation_no");
                                                                            
                        
                                                                            
                                                                           $row->[10]=$row->[10]+$row->[11];
                                                                           $row->[11]=0;
                                                                           $arr_string=join ",",@$arr_reserve;
                                                                           $db->update_query("update reservation set no_seat_assign=$row->[10],no_of_seat_remain=$row->[11],seat_number='{".$arr_string."}' where reservation_no=$row->[0]");
                                                                            
                                                                            
                                                                            
                                                                            ########## SEND MAIL OR MASG################
                                                                             my $user=$db->select_query("select ph_no,email from \"user\" where user_id='".$row->[1]."'")->[0];
                                                                             my $sms=new SMS();
                                                                             $sms->send_mail_sms($user->[0],$user->[1],$row->[0],$arr_string);
                                                               
                                                               }
                                                               else
                                                               {
                                                                           my $arr_cancel=$cancel_user->[0][12];
                                                                           my $arr_reserve=$row->[12];
                                                                           for(my $i=0;$i<$no_of_seat_cancel;$i++)
                                                                           {
                                                                                      push @$arr_reserve,pop @$arr_cancel;
                                                                           }
                                                                           
                                                                           $waiting=$waiting-$no_of_seat_cancel;
                                                                           $db->update_query("update waiting set waiting=$waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                                                           
                                                                           $row->[10]=$row->[10]+$no_of_seat_cancel;
                                                                           $row->[11]=$row->[11]-$no_of_seat_cancel;
                                                                           my $arr_string=join ",",@$arr_reserve;
                                                                           $db->update_query("update reservation set no_seat_assign=$row->[10],no_of_seat_remain=$row->[11],seat_number='{".$arr_string."}' where reservation_no=$row->[0]");
                                                                            
                                                                            
                                                                            ########## SEND MAIL OR MASG################
                                                                             my $user=$db->select_query("select ph_no,email from \"user\" where user_id='".$row->[1]."'")->[0];
                                                                             my $sms=new SMS();
                                                                             $sms->send_mail_sms($user->[0],$user->[1],$row->[0],$arr_string);
                                                                            
                                                                            $arr_string= join ",",@$arr_cancel;
                                                                            $cancel_user->[0][9]=$cancel_user->[0][9]-$no_of_seat_cancel;
                                                                            $cancel_user->[0][10]=$cancel_user->[0][10]-$no_of_seat_cancel;
                                                                            $cancel_user->[0][14]=$cancel_user->[0][14]-($price*$no_of_seat_cancel);
                                                                            $db->update_query("update reservation set no_of_seat=$cancel_user->[0][9],no_seat_assign=$cancel_user->[0][10],seat_number='{".$arr_string."}',amount=$cancel_user->[0][14]  where reservation_no=$reservation_no");
                                                                            
                                                                           
                                                               }
                                                     }
                                          }
                                  }
                                  else
                                  {
                                                      my $cancel_user=$db->select_query("select * from reservation where reservation_no=$reservation_no");
                                                      my $count=$db->select_query("select count(*) from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                                                      if($count+0==0)
                                                     {    
                                                     $db->insert_query("available_cancel",$tr_no,$class,$quota,$date,$source,$dest,0,"{}");
                                                     } 
                                                     my $avail_cancel=$db->select_query("select * from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                                     my $arr_ref_cancel=$cancel_user->[0][12];
                                                     my $arr_ref_avail=$avail_cancel->[0][7];
                                                     for(my $i=0;$i<$no_of_seat_cancel;$i++)
                                                    {
                                                              push @$arr_ref_avail,pop @$arr_ref_cancel;
                                                    }
                        
                                                    $avail_cancel->[0][6]=$avail_cancel->[0][6]+$no_of_seat_cancel;
                                                    my $arr_string=join ",",@$arr_ref_avail;
                                                    $db->update_query("update available_cancel set no_of_seat=$avail_cancel->[0][6],queue='{".$arr_string."}' where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
 
                                                    $arr_string= join ",",@$arr_ref_cancel;
                                                    $cancel_user->[0][9]=$cancel_user->[0][9]-$no_of_seat_cancel;
                                                    $cancel_user->[0][10]=$cancel_user->[0][10]-$no_of_seat_cancel;
                                                    $cancel_user->[0][14]=$cancel_user->[0][14]-($price*$no_of_seat_cancel);
                                                    $db->update_query("update reservation set no_of_seat=$cancel_user->[0][9],no_seat_assign=$cancel_user->[0][10],seat_number='{".$arr_string."}',amount=$cancel_user->[0][14]  where reservation_no=$reservation_no");
                                                    
                                                     my $reamin=$db->select_query("select seat_remain from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0] +0;
                                                     $reamin=$reamin+$no_of_seat_cancel;
                                                     $db->update_query("update waiting set seat_remain=$reamin where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                  
                                                    $no_of_seat_cancel=0;
           
                                  }
                                  
                       }
           }
           else
           {
                       my $cancel_user=$db->select_query("select * from reservation where reservation_no=$reservation_no");
                       my $count=$db->select_query("select count(*) from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0];
                       if($count+0==0)
                       {    
                                  $db->insert_query("available_cancel",$tr_no,$class,$quota,$date,$source,$dest,0,"{}");
                       } 
                        my $avail_cancel=$db->select_query("select * from available_cancel where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                        my $arr_ref_cancel=$cancel_user->[0][12];
                        my $arr_ref_avail=$avail_cancel->[0][7];
                        for(my $i=0;$i<$no_of_seat_cancel;$i++)
                        {
                                    push @$arr_ref_avail,pop @$arr_ref_cancel;
                        }
                        
                        $avail_cancel->[0][6]=$avail_cancel->[0][6]+$no_of_seat_cancel;
                        my $arr_string=join ",",@$arr_ref_avail;
                        $db->update_query("update available_cancel set no_of_seat=$avail_cancel->[0][6],queue='{".$arr_string."}' where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
 
                         $arr_string= join ",",@$arr_ref_cancel;
                         $cancel_user->[0][9]=$cancel_user->[0][9]-$no_of_seat_cancel;
                         $cancel_user->[0][10]=$cancel_user->[0][10]-$no_of_seat_cancel;
                         $cancel_user->[0][14]=$cancel_user->[0][14]-($price*$no_of_seat_cancel);
                         $db->update_query("update reservation set no_of_seat=$cancel_user->[0][9],no_seat_assign=$cancel_user->[0][10],seat_number='{".$arr_string."}',amount=$cancel_user->[0][14]  where reservation_no=$reservation_no");
                        
                        my $reamin=$db->select_query("select seat_remain from waiting where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'")->[0][0] +0;
                        $reamin=$reamin+$no_of_seat_cancel;
                        $db->update_query("update waiting set seat_remain=$reamin where date='".$date."' and tr_no=$tr_no and class='".$class."' and  quota='".$quota."' and source='".$source."' and dest='".$dest."'");
                                  
                        $no_of_seat_cancel=0;
           }



if($no_of_seat_cancel==0)
{
            
            my $amount=$db->select_query("select * from transaction where reservation_no=$reservation_no")->[0][2];
            $amount=$amount-$price*$orignal_no_of_seat_cancel;
            $db->update_query("update transaction set amount=$amount where reservation_no=$reservation_no");
            
            my $time=$db->select_query("SELECT CURRENT_TIME")->[0][0];
            my $date=$db->select_query("SELECT CURRENT_DATE")->[0][0];
            my $cancel_user=$db->select_query("select * from reservation where reservation_no=$reservation_no");
            
            $db->insert_query("cancelation",$cancel_user->[0][0],$cancel_user->[0][1],$cancel_user->[0][2],$cancel_user->[0][3],$cancel_user->[0][4],$orignal_no_of_seat_cancel,$date,$time,$amount,$source,$dest);

 print "Content-type:text/html\n\r\n\r";

 print "Cancellation done successfully for reservation number : $reservation_no.;canceled seat : $orignal_no_of_seat_cancel. ; you have got  Rs. ".$price*$orignal_no_of_seat_cancel ."  back. ";
 
                
}
}


