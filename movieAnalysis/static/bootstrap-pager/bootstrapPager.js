/**
 * js分页
 * version:0.3
 */
var Pager = function (obj) {

    this.totalCount = parseInt(obj.totalCount || 0);	//总条数
    this.pageSize = parseInt(obj.pageSize || 10);	//每页显示条数
    this.buttonSize = parseInt(obj.buttonSize || 10);//显示的按钮数
    this.pageParam = obj.pageParam || 'page';		//分页的参数,  或者要运行的JS函数名
    this.className = obj.className || 'pagination';	//分页的样式
    this.prevButton = obj.prevButton || '&laquo;';	//向前翻按钮
    this.nextButton = obj.nextButton || '&raquo;';	//向后翻按钮
    this.firstButton = obj.firstButton || '';		//第一页按钮
    this.lastButton = obj.lastButton || '';			//最后一页按钮
    this.pageIndex = obj.pageIndex || 1;             // 当前页面
    this.clickTag = obj.clickTag || 'a';
    this.useJS = obj.useJS || false;
    this.pagerName = obj.pagerName || document.getElementById("#pager");   // 用于获取分页器显示的选择器
    this.runJS = obj.runJS || this.runJS;

};


Pager.prototype.getParam = function (name) {				//获取参数
    if (this.useJS) {
        return this.pageIndex;
    } else {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    }
};


Pager.prototype.runJS = function (num) {
    console.log("这是默认的 JS 运行");
    console.log("pageIndex 用于定位当前页面");
    console.log("当前pageIndex： " + pageIndex);
};

Pager.prototype.replaceJS = function (fN, num) {
    // console.log("当前EEE " + num);
    str = 'onclick="' + fN + '(' + num + ')"';

    return str;
};

Pager.prototype.replaceUrl = function (name, value) {		//替换url参数
    var oUrl = window.location.href.replace(window.location.hash, '');
    var reg = new RegExp("(^|&)(" + name + "=)([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return 'href="' + oUrl.replace(eval('/' + r[0] + '/g'), r[1] + r[2] + value + r[4]) + '"';
    } else {
        return 'href="' + oUrl + (oUrl.indexOf('?') > 0 ? '&' : '?') + name + '=' + value + '"';
    }
};

Pager.prototype.replace = function(param, value){
    return (this.useJS ? this.replaceJS : this.replaceUrl)(param, value)
};

Pager.prototype.run = function () {


    if (this.totalCount == 0 || this.totalCount <= this.pageSize) return '';

    var page = parseInt(this.getParam(this.pageParam)) || 0;
    console.log(page);

    page = page > 1 ? page : 1;
    if (!this.useJS) {
        this.pageIndex = page;
    }
    console.log("pageIndex: " + this.pageIndex);

    var str = '<ul class="' + this.className + '">';
    if (this.firstButton) {

        str += `
                <li class="page-item">
                    <${this.clickTag} class="page-link"  ${this.replace(this.pageParam, 1)}>${this.firstButton}</${this.clickTag}>
                </li>
            `;
    }
    if (page <= 1) {
        str += `
                <li class="page-item disabled">
                    <${this.clickTag} class="page-link">${this.prevButton}</${this.clickTag}>
                </li>
            `;
    } else {
        str += `
                <li class="page-item">
                    <${this.clickTag} class="page-link" ${this.replace(this.pageParam, this.pageIndex - 1)} >${this.prevButton}</${this.clickTag}>
                </li>
            `;
    }
    console.log("run   pageindex " + this.pageIndex);
    var max = Math.ceil(this.totalCount / this.pageSize);
    var start = Math.floor((page - 2) / (this.buttonSize - 2)) * (this.buttonSize - 2);
    start = start + this.buttonSize > max ? max - this.buttonSize : start;
    start = start >= 0 ? start : 0;
    for (var i = start + 1; i <= start + this.buttonSize; i++) {
        if (i > max || this.buttonSize < 3) break;
        str += `
                <li ${(i == this.pageIndex ? ' class="page-item active"' : '')} >
                    <${this.clickTag} class="page-link"  ${this.replace(this.pageParam, i)}>${i}</${this.clickTag}>
                </li>
            `;
    }
    if (page >= max) {
        str += `
                <li class="page-item disabled">
                    <${this.clickTag} class="page-link">${this.nextButton}</${this.clickTag}>
                </li>
            `;
    } else {
        str += '';
        str += `
                <li class="page-item">
                    <${this.clickTag} class="page-link" ${this.replace(this.pageParam, this.pageIndex + 1)}>${this.nextButton}</${this.clickTag}>
                </li>
            `;
    }
    if (this.lastButton) {
        str += '';
        str += `
                <li class="page-item">
                    <${this.clickTag} class="page-link" ${this.replace(this.pageParam, max)}>'${this.lastButton}</${this.clickTag}>
                </li>
            `;
    }
    str += '</ul>';
    // console.log(str);
    // pagerName.empty();
    this.pagerName.innerHTML = str;
    // return str;
};
