#!/usr/bin/perl -w
use strict;
use warnings;
package SMS;

use MIME::Lite;
use Net::SMS::WAY2SMS;



sub new{
              my $class=shift;    
              return bless {},$class;
}


sub send_mail_sms{
shift;
my $phno=shift;
my $email=shift;
my $reservation_no=shift;
my $seat=shift;
my $massage="hi,your reservation_no=$reservation_no, Check your status from web-site. \nthank you.";#and seat_no=$seat \nthank you.";


 
my $s = Net::SMS::WAY2SMS->new(
                'user' => '9099284839' ,
                'password' => '4475112',
                'mob'=>["$phno"]
        );
 
eval{$s->send("$massage");};
      
 MIME::Lite->send ("smtp", "inf1mail.flightnetwork.com"); 
my $msg = MIME::Lite->new
  (
  From    => 'Train.reservation@farematrix.com',
  To      =>"$email",
  Data    => "$massage",
  Subject => "train reservation detail",
  );
 eval{ $msg->send();}
    
  }

 sub send_password{
shift;

my $phno=shift;
my $email=shift;
my $password=shift;

my $massage="hi,your password is $password . \nthank you.";#and seat_no=$seat \nthank you.";


 
my $s = Net::SMS::WAY2SMS->new(
                'user' => '9099284839' ,
                'password' => '4475112',
                'mob'=>["$phno"]
        );
 eval{$s->send("$massage");};
 MIME::Lite->send ("smtp", "inf1mail.flightnetwork.com"); 
my $msg = MIME::Lite->new
  (
  From    => 'Train.reservation@farematrix.com',
  To      =>"$email",
  Data    => "$massage",
  Subject => "train reservation detail",
  );
 eval{ $msg->send();};
  } 
  
1
