import dpath.util
a = {264689818: {'1383024': {'data': [
    'Название отеля: Carlton\nАдрес отеля: Birkenhead Street, London, England, WC1H 8BA\nРейтинг отеля: \nСтоимость отеля: от 495$ до 736$\n'],
                             'photo': [
                                 'https://images.trvl-media.com/lodging/2000000/1390000/1383100/1383024/2be85538.jpg?impolicy=resizecrop&rw=500&ra=fit',
                                 'https://images.trvl-media.com/lodging/2000000/1390000/1383100/1383024/3c1ff880.jpg?impolicy=resizecrop&rw=500&ra=fit']},
                 '1223173': {'data': [
                     "Название отеля: OYO Grantly Hotel, London Shepherd's Bush\nАдрес отеля: 50 Shepherds Bush Green, London, England, W12 8PS\nРейтинг отеля: 7.4/10 Good\nСтоимость отеля: от 500$ до 623$\n"],
                             'photo': [
                                 'https://images.trvl-media.com/lodging/2000000/1230000/1223200/1223173/e8e459b6.jpg?impolicy=resizecrop&rw=500&ra=fit',
                                 'https://images.trvl-media.com/lodging/2000000/1230000/1223200/1223173/1965882c.jpg?impolicy=resizecrop&rw=500&ra=fit']},
                 '9093425': {'data': [
                     'Название отеля: Mandalay Picton House Hotel\nАдрес отеля: 122 Sussex Gardens, London, England, W2 1UB\nРейтинг отеля: 7.0/10 Good\nСтоимость отеля: 506$\n'],
                             'photo': [
                                 'https://images.trvl-media.com/lodging/10000000/9100000/9093500/9093425/c00f42a6.jpg?impolicy=resizecrop&rw=500&ra=fit',
                                 'https://images.trvl-media.com/lodging/10000000/9100000/9093500/9093425/c4086737.jpg?impolicy=resizecrop&rw=500&ra=fit']}}}

for i in a[264689818]:
    print(a[264689818][i]['data'])
    print(a[264689818][i]['photo'])
    print()
