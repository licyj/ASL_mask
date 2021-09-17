# label-modify

## usage
請大家先執行以下程式
確保標註資料沒有錯誤再上傳
使用apply_mask視覺化標註結果影片看是否順暢，都有標註到再上傳


## 可能問題
中間如果跳錯，高機率是有某個label沒有標上類別 請注意

## 結構
https://imgur.com/DSpsuB4

https://imgur.com/C4Ej7hD


```
  python json2png.py {path/to/your/root/label_fodler} {path/to/mask_folder}
```
eg: python json2png.py jsons masks
如果有錯誤的話，會在終端機上印出哪個資料夾的哪個標註json檔案有誤

- 參數1: 放所有標注資料的root directory
- 參數2: 指定一個放置mask的地方
-h 選項可以看說明


```
  python applymask.py {path/to/mask_folder} {path/to/output_video_folder}
```
eg:  python applymask.py masks output_video_folder
- 參數1: 上述程式指定放mask的地方
- 參數2: 輸出 video的目標資料夾
-h 選項可以看說明
