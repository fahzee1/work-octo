var Cart = function(cookie_name, equipment_total_class, monthly_total_class, equipment_breakdown_class, current_equ) {
    this.cookie_name = cookie_name;
    this.cart = getCookie(this.cookie_name);
    if(!this.cart) {
        this.reset();
    }else{
        this.cart = JSON.parse(this.cart); 
    }
    this.equipment_total_class = equipment_total_class;
    this.monthly_total_class = monthly_total_class;
    this.equipment_breakdown_class = equipment_breakdown_class;
    this.render();
}

$.extend(Cart.prototype, {
    debug: function() {
        console.log(this.cart);
    },
    reset: function() {
        this.cart = {'monitoring': {}, 'package': {}, 'equipment': {}};
        setCookie('paCart', JSON.stringify(this.cart));
    },
    save: function() {
        setCookie(this.cookie_name, JSON.stringify(this.cart));
        this.render();
    },
    add_monitoring: function(item, price, moprice) {
        this.cart['monitoring'] = {'item': item, 'price': price, 'monthly': moprice};
        this.save();
    },
    add_package: function(item, price, moprice) {
        this.cart['package'] = {'item': item, 'price': price, 'monthly': moprice};
        this.save();
    },
    add_equipment: function(item, price, moprice) {
        if(!this.cart['equipment'][item]) {
            this.cart['equipment'][item] = {'price': price, 'count': 0, 'monthly': moprice};
        }
        this.cart['equipment'][item]['count'] = (this.cart['equipment'][item]['count'] + 1);
        this.save();
    },
    add_to_cart: function(category, item, price, moprice) {
        switch(category) {
            case 'equipment':
                this.add_equipment(item, price, moprice);
                break;
            case 'monitoring':
                this.add_monitoring(item, price, moprice);
                break;
            case 'package':
                this.add_package(item, price, moprice);
                break;
        }
    },
    remove_equipment: function(item) {
        if(!this.cart['equipment'][item]) {
            return false;
        }
        this.cart['equipment'][item]['count'] = (this.cart['equipment'][item]['count'] - 1);
        if(this.cart['equipment'][item]['count'] == 0) {
            delete this.cart['equipment'][item];
        }
        this.save();
    },
    remove_category: function(category) {
        this.cart[category] = {};
        this.save();
    },
    remove_from_cart: function(category, item) {
        switch(category) {
            case 'equipment':
                this.remove_equipment(item);
                break;
            case 'monitoring':
                this.remove_category(category);
                break;
            case 'package':
                this.remove_category(category);
                break;
        }
    },
    get_equipment_total: function() {
        var equipment_total = Number(0.00);
        $.each(this.cart['equipment'], function(i, equip) {
            equip_item_total = equip.count * equip.price;
            equipment_total = equipment_total + Number(equip_item_total);
        });
        return equipment_total;
    },
    get_equipment_monthly: function() {
        var total = Number(0.00);
        $.each(this.cart['equipment'], function(i, equip) {
            equip_item_total = equip.count * equip.monthly;
            total = total + Number(equip_item_total);
        });
        return total;
    },
    get_monthly_total: function() {
        var monthly_total = Number(0.00);
        if(this.cart['monitoring']) {
            monthly_total = monthly_total + Number(this.cart['monitoring']['monthly']);
        }
        if(this.cart['package']) {
            monthly_total = monthly_total + Number(this.cart['package']['monthly']);
        }
        monthly_total = monthly_total + this.get_equipment_monthly();
        return monthly_total;
    },
    render: function() {
        $('.'+this.equipment_total_class).html(this.get_equipment_total());
        $('.'+this.monthly_total_class).html(this.get_monthly_total());
        var breakdown = $('<ul/>');
        $.each(this.cart['equipment'], function(i, equip) {
            $('<li/>').html(
                    i + ' : ' + equip.count + 
                    ' : $' + Number(equip.count * equip.price) + 
                    '<div class="remove_from_cart">-</div>').
                attr('data-category', 'equipment').
                attr('data-item', i).
                appendTo(breakdown);
        });
        $('.'+this.equipment_breakdown_class).html(breakdown);
    },
});