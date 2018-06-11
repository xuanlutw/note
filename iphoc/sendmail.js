const nodemailer = require("nodemailer");
const data = require("./data.json")

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: "",
    pass: ""
  }
}); 


function send_mail(data) {
    var mailOptions = {
        from: 'iphocamp',
        to: data["mail"],
        attachments: [
            {
                filename: '家長同意書.pdf',
                path: './家長同意書.pdf'
            },
            {
                filename: '匯退款資訊.pdf',
                path: './匯退款資訊.pdf'
            }
        ]
    };
    mailOptions.subject = data['name'] + "-IPhOC暑期奧林匹亞物理營錄取通知";
    mailOptions.text = 
        data["name"] + "你好：\n\n" + 
        "        恭喜你成功錄取 2018 IPhOC 暑期奧林匹亞物理營，請先確認下列資訊是否正確。\n" +
        "                名字： " + data["name"] + "\n" +
        "                性別： " + data["a"] + "\n" +
        "                身分證字號： " + data["b"] + "\n" +
        "                出生日期： " + data["c"] + "\n" +
        "                連絡電話： " + data["f"] + "\n" +
        "                電子信箱： " + data["mail"] + "\n" +
        "                住址： " + data["g"] + "\n" +
        "                家長姓名： " + data["h"] + "\n" +
        "                關係： " + data["i"] + "\n" +
        "                家長電話： " + data["j"] + "\n" +
        "                飲食禁忌： " + data["k"] + "\n" +
        "                其他注意事項：" + data["l"] + "\n" +
        "                營服尺寸(S/M/L)請麻煩額外填寫： \n\n" +
        "        另請於6/19（含）前將報名費新台幣4000元整匯款至下列郵局(代號700)帳戶：\n" + 
        "                姓名：xxx\n                戶號：xxx-xxx\n\n" + 
        "        匯款後請儘速回覆此信，告知個人資料是否正確、營服尺寸、匯款時間、匯款人及匯款帳號末五碼，並附上家長同意書（掃描或清楚照片），我們會於三個工作天內回信確認匯款事宜。若逾期未回信將視同放棄本次營隊錄取資格。\n\n" + 
        "        如有任何疑問，請寄信至此信箱詢問。\n\n" + 
        "                IPhOC 籌備團隊 敬上\n                20180611"
    transporter.sendMail(mailOptions, function(error, info){
        if (error) {
            console.log(error);
            console.log(data);
        } else {
            console.log('Email sent: ' + info.response);
        }
    });
}

for (var i = 0; i < data.length; i++) {
    setTimeout(send_mail, 2000 * i, data[i])
}
