import fs from 'fs'
import { Buckets, UserAuth, KeyInfo } from '@textile/hub'

var myArgs = process.argv.slice(2);
console.log('myArgs: ', myArgs);


(async () => {
  const keyInfo: KeyInfo = {
    key: 'XXXXXXXXXXXXXXXXXXXXXXXX',
    secret: 'XXXXXXXXXXXXXXXXXXXXXXX'
  }
  const buckets = await Buckets.withKeyInfo( keyInfo );
  const createOrGetResult = await buckets.getOrCreate("VidNftHubJs0");
  const bucketKey = createOrGetResult.root.key;
  console.log(bucketKey)

  let file = myArgs[0]
  const filePath = "../assets/" + file
  var content = fs.createReadStream(filePath, { highWaterMark: 1024 });
  const upload = {
    path: file,
    content
  }

  let result = await buckets.pushPath(bucketKey!, file, upload)
  console.log(result)
})();