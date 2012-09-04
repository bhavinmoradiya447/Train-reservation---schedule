package Encrypt_decrypt;
use warnings;
use strict;
use Crypt::CBC;
use Crypt::Blowfish;



my $key;# = "projectonrailway";  

my $cipher;# = Crypt::CBC->new( -key    => "$key",
                       #      -cipher => 'Blowfish',
                         #  );

sub new
{
    my $class=shift;
    $key = "projectonrailway";  
    $cipher = Crypt::CBC->new( -key    => "$key",
                             -cipher => 'Blowfish',
                           );

   return bless {},$class;
}


sub encrypt{
return $cipher->encrypt($_[1]); 
 }

sub decrypt{
return  $cipher->decrypt($_[1]);
    }

# my $e=new Encrypt_decript();
# my $ciphertext = $e->encrypt("3769-198501-21002"); 
# print "$key\n";
# print "$ciphertext\n";

# # my $plaintext  =$e->decrypt($ciphertext);
# print "$plaintext\n";




1