

head = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>Check Result</title>
</head>'''

css = '''<style type="text/css">
*
{
    padding:0;
    margin:0;
}
body {
    background-color: #f6f6f6;
}

.left {
    float: left;
}

.right {
    float: right;
}

.container {
    margin: 0px auto;
    width: 100%;
}

#header {
    background-color: #f5f9fa;
    height: 40px;
    border-bottom: 1px inset #fff;
    box-shadow: 10px 0px 20px #dddde8;
}

.header_right .text {
    display: inline-block;
    text-decoration-style: none;
    margin-left: 10px;
    margin-right: 10px;
    line-height: 40px;
    font-size: 16px;
}

.nav {
    padding-right: 10px;
}

.header_left .logo {
    display: inline-block;
    line-height: 40px;
}
#main {
    margin-left: 40px;
}
#show{
    height:575px;
    margin-top:30px;
}
#show .container{
    margin:10px auto;
    background-color:#FFFAFA;
    border-radius:5px;
    border:2px solid #333;
    height:575px;
    width:1343px;
}
#show .container #head{
    height:58px;
    border-bottom:3px solid #333;
}
#show .container #content_left{
    width:670px;
    float:left;
    border-right:2px solid #333;
    height:465px;
    color:#333;
}
#show .container #content_right{
    width:670px;
    float:right;
    height:465px;
    color:#333;
}
#show .container #bottom{
    height:48px;
    border-top:2px solid #333;
    clear:both;
}
</style>'''

filename1_before = '''<body>
    <div id="header">
        <div class="container">
            <div class="header_left left">
                <div class="logo"><span id="text_" class="left" style="color:#333333;font-size:20px; font-weight:650;margin-left:20px">CodeChecker</span></div>
            </div>
        </div>
    </div>
    <div id="show">
        <div class="container">
            <div id="head">
                <div  style="display:inline-block;width:509px;height:58px;line-height:58px;font-size:18px;color:#333;margin-left:100px">
                    <span id="left_file" style="text-align:center;margin:0px auto;width:509px;height:58px;display:inline-block;font-size:23px">
'''

filename1_sim = '''</span>
                </div>
                <div  style="display:inline-block;width:140px;height:58px;line-height:58px;color:red;font-weight:650;font-size:18px;margin-left:1px">
                    <span style="text-align:center;margin:0px auto;width:140px;height:58px;display:inline-block;font-size:21px">
'''

sim_filename2 = '''</span>
                </div>
                <div  style="display:inline-block;width:406px;margin-left:20px;color:#333;font-size:18px;line-height:58px;height:58px">
                    <span id="right_file" style="text-align:center;margin:0px auto;width:406px;height:58px;display:inline-block;font-size:23px">
'''

filename2_content1 = '''</span>
                </div>
            </div>

            <div id="content_left" style="overflow:scroll" >
                <p style="color:#333;font-size:16px">
'''

content1_content2 = '''</p>
            </div>
            <div id="content_right" style="overflow:scroll">
                <p style="color:#333;font-size:16px">
'''

end = '''</p>
            </div>


            <div id="bottom" style="position:relative;border-bottom:2px solid #333"></div>

            </div>
        </div>
    </div>
</body>
</html>
'''


def generate_html(filename1, sim, filename2, content1, content2, path):
    file = head + css + filename1_before + filename1 + filename1_sim + sim + sim_filename2 + filename2 + filename2_content1 + content1 + content1_content2 + content2 + end
    open(path, 'w').write(file)
