# Run without patching
verifyBug.sh $1

# Prove all bugs
for f in certora/tests/$1/bug*.patch
do
    wildcard=${f##"certora/tests/$1"/bug}
    wildcard=${wildcard%.patch}
    verifyBug.sh $1 $wildcard
done