import React ,{Component} from 'react';
import {View,Button} from 'react-native';
import ImagePicker from 'react-native-image-crop-picker';
let SERVER_URL = 'http://url:8888/'
let BUCKET_URL = 'http://bucketname.endpoint'
export default class App extends Component {
  async upload(img) {
    await fetch(SERVER_URL, {
      headers: {'content-type': 'application/json'}
    })
      .then(response => response.json())
      .then(responseData => {
        let formdata = new FormData();
        formdata.append("key", responseData['dir'] + '${filename}')
        formdata.append("policy", responseData['policy'])
        formdata.append("OSSAccessKeyId", responseData['accessid'])
        formdata.append("success_action_status", '200')
        formdata.append("signature", responseData['signature'])
        formdata.append("file", { uri: img.uri, name: img.filename, type: img.mime })
        fetch(BUCKET_URL, { method: 'post', headers: { 'Content-Type': 'multipart/form-data' }, body: formdata })
         .then((response) => response.text())
         .then((responsedata) => {
         console.log(responsedata,'success')
         })
      });
  }

  async pickSingle(cropit, circular = false, mediaType) {
    await ImagePicker.openPicker({
      width: 100,
      height: 100,
      cropping: cropit,
      cropperCircleOverlay: circular,
      sortOrder: 'none',
      compressImageMaxWidth: 1000,
      compressImageMaxHeight: 1000,
      compressImageQuality: 1,
      compressVideoPreset: 'MediumQuality',
      includeExif: true,
    }).then(image => {
      let filename = Date.now() + '.' + image.mime.split('/')[1]
      let img = { uri: image.path, width: image.width, height: image.height, mime: image.mime, filename: filename }
      this.upload(img)
    }).catch(e => {
      console.log(e);
    });
    
  }


  render() {
    return(
      <View><Button title='点我上传文件' onPress={()=>this.pickSingle()}></Button></View>
  )}
}