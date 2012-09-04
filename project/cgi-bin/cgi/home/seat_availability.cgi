#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;

BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
my $db=new Database();


my $template=new HTML::Template(filename=>'../../html/home/seat_availability.tmpl'); 



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

$template->param(TRAIN_NO=>&tr_no); # to set  train  number
$template->param(TRAIN_SOURCE=>&tr_source);#to set train source;
$template->param(TRAIN_DEST=>&tr_dest);#to set train source;



print "Content-type:text/html\n\r\n\r";
print $template->output;

