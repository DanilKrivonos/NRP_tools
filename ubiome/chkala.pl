#!/bin/env perl

use strict;
use warnings;

my %c = ();
open my $efh, '<', 'all.ens.tsv' or die $!;
while(<$efh>){
    chomp;
    my($dom, $meth, $call) = split(/\t/, $_);
    if($call eq 'ala'){
	$c{$dom}{'ens'} = $call;
    }
}
close $efh;
my %method = (
    'ens' => 1
);
open my $ifh, '<', 'all.ind.tsv' or die $!;
while(<$ifh>){
    chomp;
    my ($dom, $meth, $call) = split(/\t/, $_);
    if(exists $c{$dom}){
	$c{$dom}{$meth} = $call;
    }
    $method{$meth} = 1 unless(exists $method{$meth});
}
close $ifh;
print '#'.join('_', sort keys %method)."\n";
my %s = ();
foreach my $d (keys %c){
    my $str = '';
    foreach my $m (sort keys %{$c{$d}}){
	if($str eq ''){
	    $str = $c{$d}{$m};
	}else{
	    $str .= '_'.$c{$d}{$m};
	}
    }
    $s{$str} += 1;
}
print '#'.scalar(keys %c)."\n";
foreach my $str (sort {$s{$b} <=> $s{$a}} keys %s){
    print join("\t", $s{$str}, $str)."\n";
}
