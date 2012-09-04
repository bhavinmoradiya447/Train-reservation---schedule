#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;

BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
my $db=new Database();
sub tr_no{
my $result=$db->get_train_no();
my $data=[];
foreach(@$result)
{
push @$data,{TR_NO=>$_};
#=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
}
return $data;
}

sub tr_name{
my $result=$db->get_train_name();
my $data=[];
foreach(@$result)
{
push @$data,{TR_NAME=>$_};
#=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
}
return $data;
}


sub st_name{
    
my $result=$db->get_station_name();
my $data=[];
foreach(@$result)
{
push @$data,{ST_NAME=>"$_->[0] - $_->[1]"};
#=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
}
return $data;
}

my $template=new HTML::Template(filename=>'../../html/home/station_information.tmpl'); 

$template->param(TRAIN_NO=>&tr_no); # to set  train  number
$template->param(TRAIN_NAME=>&tr_name); # to set  train  name
$template->param(STATION_NAME=>&st_name); # to set  station  name


print "Content-type:text/html\n\r\n\r";
print $template->output;
