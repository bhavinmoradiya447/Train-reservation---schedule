#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;

my $template=new HTML::Template(filename=>'../../html/temp/login.tmpl'); 

print "Content-type:text/html\n\r\n\r";
print $template->output;
