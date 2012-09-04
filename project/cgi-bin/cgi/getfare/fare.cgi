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

my($tr_no,$source,$dest,$class,$day,$month,$year,$cons)=($cgi->param("tr_no_drop_down"),$cgi->param("tr_source_drop_down"),$cgi->param("tr_dest_drop_down"),$cgi->param("tr_class_drop_down"),$cgi->param("lccp_day"),$cgi->param("lccp_month"),$cgi->param("lccp_year"),$cgi->param("tr_cons_drop_down"));
my $date="$day-$month-$year";
my $template=new HTML::Template(filename=>'../../html/getfare/fare.tmpl'); 

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
                # else
                # {
                  # print "Content-Type: text/html\n\n";
                                # print<<end
                                # <html>
                                # <head>
                                # <script type="text/javascript">
                                # alert("Invalid Source and Destination");
                                # window.location="/cgi-bin/getfare/getfare.cgi";
                                # </script>
                                # </head>
                                # <body><p>Loading, please wait ...</p></body>
                                # </html>

# # end

# }
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

$template->param(TR_NO=>$tr_no); # to set  train  number
$template->param(TR_NAME=>&tr_name);
$template->param(DATE=>$date);
$template->param(TR_SOURCE=>$db->select_query("select station_name from station where station_code='".$source."'")->[0][0]); # to set  train  source
$template->param(TR_DEST=>$db->select_query("select station_name from station where station_code='".$dest."'")->[0][0]); # to set  train  destination
$template->param(TR_TYPE=>&tr_type);
$template->param(DIST=>&distance);
$template->param(CLASS=>$class);
$template->param(FARE=>&fare);
$total+=20;
if($is_super_fast eq "true")
{
$total+=30;
 $template->param(SUPER_CHARGE=>30);
}
else
{
 $template->param(SUPER_CHARGE=>0);
}

$concession=$price*$distance*$cons/100;
$template->param(CONC=>$concession); # to set  train  concession

$total-=$concession;
$template->param(TOTAL=>$total);

print "Content-type:text/html\n\r\n\r";
print $template->output;
