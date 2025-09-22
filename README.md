# novels_scraping
基于playwright，可以通过cloudflare的检测

我参照的小说是https://www.beqege.cc/65200/

偶然间发现他们家的防护是cloudflare做的。或许是因为自己就是爬虫起家？（说是笔趣阁但谁知道呢？）反正反爬算是比较严格的，静态库解决不了，selenium还会被检测出来，于是用了playwright

中间写的可能啰里啰唆的，反正看个框架就行了。速度可以自己调，反正我设的非常保守，1000章用了三个半小时（别给封IP就行，cloudflare的IP检测非常麻烦）

顺便安利一下这本小说：《我的治愈系游戏》，写的还挺有意思的
<img width="2272" height="1282" alt="image" src="https://github.com/user-attachments/assets/65c943fa-e395-421e-ab68-7cff2292dc2d" />


有一个问题：

Pycharm一直给这一段标黄：

        context = await browser.new_context(

                viewport= {'width':2560, 'height':1440},  # type: ignore <---这里被标黄了
        
                user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        
            )
    
我看文档里也有类似的写法，不知道为什么会被认为有错，不过不影响运行，我把它忽略了
