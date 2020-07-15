#### 使用说明

- 运行server:
    - 下载项目代码 git clone https://github.com/Brightest08/rn-aliyun-oss
    - 修改docker-compose.yaml文件，配置阿里云秘钥相关信息:
        - 1、ACCESS_KEY_ID 请填写您的AccessKeyId
        - 2、ACCESS_KEY_SECRET 请填写您的AccessKeySecret
        - 3、HOST host的格式为 bucketname.endpoint ，请替换为您的真实信息
        - 4、CALLBACK_URL callback_url为 上传回调服务器的URL，请将下面的IP和Port配置为您自己的真实信息
        - 5、EXPIRE_TIME 生成token的有效期
        - 6、UPLOAD_DIR 用户上传文件时指定的前缀
        - 具体相关配置请参考 https://help.aliyun.com/document_detail/91848.html?spm=a2c4g.11186623.2.16.47376e28QY0RrH#concept-ynl-hky-2fb
    - docker-compose up -d 运行server
	
- 运行client demo
  - 替换 client/demo/App.js中SERVER_URL，BUCKET_URL相应地址
  - yarn
  - react-native run-android
  - ~ 记一个小bug，由于升级了rn版本，在上传图片的时候一直报网络错误，具体解决办法参考 https://github.com/facebook/react-native/issues/28551