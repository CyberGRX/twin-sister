#!/bin/bash
if test 'master' == "$TARGET_BRANCH"; then
  twine upload --repository-url $NEXUS_URL -u $NEXUS_USERNAME -p $NEXUS_PASSWORD `ls dist/*.whl | head -n1`
else
  echo "Choosing not to upload the package from $TARGET_BRANCH branch to Nexus"
fi
