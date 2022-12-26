// index.js
// 获取应用实例
import '../../serverURL'
import { serverURL } from '../../serverURL'
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName'), // 如需尝试获取用户信息可改为false
    src: null,
    date: null,
    latitude: null,
    longitude:null,
    ocr: null,
  },

  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },

  takePhoto: function() {
    this.setData({
      date: (new Date()).toISOString(),
    })
    let ctx = wx.createCameraContext();
    wx.getLocation().then((res) => {
      this.setData({
        latitude: res.latitude,
        longitude: res.longitude,
      })
    });
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          src: res.tempImagePath,
        });
      }
    });
  },

  postImage: function() {
    console.log(this.data.src)
    wx.uploadFile({
      url: serverURL,
      filePath: this.data.src,
      name: "img",
      success: (res) => {
        this.setData({
          ocr: res.data
        })
      }
    });
  },
})
