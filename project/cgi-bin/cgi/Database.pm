#!/usr/bin/perl -w
package Database;
use warnings;
use strict;
use DBI;

my $dbh;
sub new{   #creating Object 
              my $class=shift;    
             $dbh=DBI->connect("DBI:Pg:dbname=Project;host=localhost","bhavin","bhavin");
              return bless {},$class;
}

sub user_validation{        # Check that whether username exist or not
              my $username=$_[1];
             my $result=$dbh->prepare("SELECT COUNT(*) FROM \"public\".\"user\" WHERE \"user_id\" = ?");
             $result->bind_param(1,$username);
             $result->execute();
             while (my $arr=$result->fetchrow_arrayref())
              {
                  if($arr->[0]>0){return "true";}
                  else{return "false";}
              }
}

sub login_validation{        # Check that whether username and password exist or not
              my $username=$_[1];
              my $password=$_[2];
              my $result=$dbh->prepare("SELECT COUNT(*) FROM \"public\".\"user\" WHERE \"user_id\" = ? AND \"password\" = ? ");
             $result->bind_param(1,$username);
             $result->bind_param(2,$password);
             $result->execute();
             while (my $arr=$result->fetchrow_arrayref())
                 {
                   if($arr->[0]>0){
                             my $update= $dbh->prepare("UPDATE \"public\".\"user\" SET \"last_date\"=current_date ,\"time\"=current_time WHERE \"user_id\"=? AND \"password\"=?" );
                             $update->bind_param(2,$password);
                             $update->execute();
                             return "true";
                             }
                            else{return "false";}
                }
}


sub insert_query{           # insert query for insert into any table
                 my($class,$table,@param)=@_;
                 my $query="INSERT INTO \"public\".\"".$table."\" VALUES (?";
                 for(my $i=1;$i<@param;$i++)
                  {
                    $query.=",?";
                  }
                 $query.=")";
 
                  my $result=$dbh->prepare($query);
                  for(my $i=0;$i<@param;$i++)
                   {
                       $result->bind_param($i+1,$param[$i]); 
                   }
 
                   $result->execute();
                   if($result->err)
                  {
                          if($result->errstr=~m/date/i)
                           {return "date_error";}
                           else{return "error occor";}
                  }
                else{return "true";}
 }


sub fatch_username{
                             my $username=$_[1];
                             my $result=$dbh->prepare("SELECT \"name\" FROM \"public\".\"user\" WHERE \"user_id\" = ?");
                             $result->bind_param(1,$username);
                             $result->execute();
                             my $name;
                             while (my $arr=$result->fetchrow_arrayref())
                                   {
                                    return @$arr;
                                   }
                            return $name;
}
 
 sub get_train_no{
                             my $result=$dbh->prepare("SELECT \"tr_no\" FROM \"public\".\"train\" ");
                             $result->execute();
                             my $name=[];
                            while (my $arr=$result->fetchrow_arrayref())
                                  {
                                    push @$name, @$arr[0];
                                   }
                            return $name;
}

 sub get_train_name{
                      my $result=$dbh->prepare("SELECT \"tr_name\" FROM \"public\".\"train\" ");
                      $result->execute();
                       my $name=[];
                      while (my $arr=$result->fetchrow_arrayref())
                         {
                          push @$name, @$arr[0];
                         }
                        return $name;
}
sub get_station_name{
                         my $result=$dbh->prepare("SELECT \"station_name\",\"station_code\" FROM \"public\".\"station\" order by station_name ");
                        $result->execute();
                        my $name=[];    
                        while (my $arr=$result->fetchrow_arrayref())
                         {
                               push @$name, [@$arr[0],@$arr[1]];
                         }
                       return $name;
 }

sub select_query{
                     shift;
                     my $query=shift;
                     my $result=$dbh->prepare($query);
                    $result->execute();
                     my $name=[];
                    while (my $arr=$result->fetchrow_arrayref())      
                      {
                       my $arr_ref=[];
                      foreach(@$arr)                    # every time create new array ref of each facthed row array ref, and gnerate array of array;
                          {
                          push @$arr_ref,$_;
                          } 
                        push @$name, $arr_ref;

                     }
                 return $name;     # i.e [ [value1,value2,..] ,[value1,value2,..] ,[value1,value2,..] ]
 
}

sub update_query{
                     shift;
                     my $query=shift;
                     my $result=$dbh->prepare($query);
                    $result->execute();
 }

END{
 $dbh->disconnect();
};
1
