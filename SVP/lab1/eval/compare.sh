if diff --strip-trailing-cr $1 $2 > /dev/null
then
   echo "The files match"
else
   echo "The files are different"
fi