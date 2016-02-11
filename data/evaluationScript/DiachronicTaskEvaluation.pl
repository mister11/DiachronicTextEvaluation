system("clear");

print "\n\n\nUsage::: perl DiachronicTaskEvaluation.pl file1 file2 granularity\n";
print "Usage::: file1 is the goldStandard annotation name file\n";
print "Usage::: file2 is the machine annotation name file\n";
print "Usage::: granularity is a string , one and only one of these- textF, textM or textC - showing what granularity of the task is evaluated\n";
print "\n\n\n";


open (fg, $ARGV[0]); ## this is the gold standard
open (fm, $ARGV[1]); ## this is the machine output

$g = $ARGV[2]; ## this is the grade that is evaluated
               ## textF, textM, textC
               ## for fine, medium or coarse evaluation respectively 
            

### defining the scale ###
### each individual answer is evaluated from 0 to 0.99 ###
### 0 is a perfect prediction - same interval ###
### 0.99 is at least 8 intervals off ###
### 0.99 represents approx. 50, 100 and 150 years off, for fine, medium and coarse evaluation respectively ###

$yearSpan{"textF"} = 6; $yearSpan{"textM"} = 12; $yearSpan{"textC"} = 20;

### the scale can be modified as desired by modifying the weights below ###
$scale[0] = 0;     ### the same interval prediction
$scale[1] = 0.1;   ### one interval off
$scale[2] = 0.15;  ### two intervals off
$scale[3] = 0.2;   ### three intervals off
$scale[4] = 0.4;   ### four intervals off
$scale[5] = 0.5;   ### five intervals off
$scale[6] = 0.6;   ### six intervals off
$scale[7] = 0.8;   ### seven intervals off
$scale[8] = 0.9;   ### eight intervals off
$scale[9] = 0.99;  ### nine intervals or MORE off
### the scale can be modified as desired by modifying the weights above ###

$scaleMaxOff = $#scale;  ## all answers that are off more than scale, are weighted the same

$i = 0; while ($i <= $scaleMaxOff) { $hic{$i} = $yearSpan{$g} * $i; $i++};

## if the machine does not offer an answer , no "yes=", then for that piece of news the score is considered 0.99 ##
## however, we compute separately the true precision  = fraction of the correct guesses ##

while (<fg>)
{
	chomp;
	if ($_ !~ /^<$g /) { next;}
	$nr++;
	$lg = $_; 
	$ig = $lg; @ag = split ' ', $lg; 
	$ig = -1; $i = 0; while ($i <= $#ag) { if ($ag[$i] =~ /yes=\"/) { $ig = $i; last} $i++;}
	
	$lm = <fm>; chomp ($lm);
	while ($lm !~ /^<$g / && !eof(fm))
	{
		$lm = <fm>; chomp($lm);
	}
	$im = $lm; @am = split ' ', $lm; 
	$im = -1; $i = 0; while ($i <= $#am) { if ($am[$i] =~ /yes=\"/) { $im = $i; last} $i++;}
	
	$indScore = abs($ig-$im);
	if ($im == -1 || $indScore >= $scaleMaxOff) { $indScore = $scaleMaxOff;}
	
	
	
	if ($im != -1) { $tries++};
	
	push @score, $scale[$indScore];
	
	$hc{$indScore}++;
	
	$ss = $ss + $yearSpan{$g} * $indScore;
	
	$medSum = $medSum + $scale[$indScore];
	
}

close fg; close fm;

$med = 1 - int($medSum / $nr *10000)/10000;
print "************\n";
print "Score $med\n";
print "************\n\n";

$prec = int ($hc{0}/$tries*10000)/10000;
print "Precision $prec\n";
print "Tried $tries out of $nr\n";
$ayo = int ($ss / $nr);
print "Average years off $ayo\n\n";

print "Distribution of predictions:\n";
$i = 0; while ($i <= $#scale) { if (!defined($hc{$i})) {$hc{$i} = 0};print "There are $hc{$i} predictions which are off $hic{$i} years\n"; $i++; }
print "\n";







	


