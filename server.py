#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi, db

PORT_NUMBER = 8000

class myHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path=="/":
            self.path = "index.html"
        elif self.path == "/order/create":
            self.path = "order_create.html"
        elif self.path == "/order/viewall":
            self.path = "order_viewall"
        elif self.path == "/maintenance/viewall":
            self.path = "maintenance_viewall"
        elif self.path == "/qa/viewall":
            self.path = "qa_viewall"
        elif self.path == "/order/view":
            self.path = "order_view.html"
        elif self.path == "/maintenance/view":
            self.path = "maintenance_view.html"
        elif self.path == "/order/update":
            self.path = "order_update.html"
        elif self.path == "/maintenance/create":
            self.path = "maintenance_create.html"
        elif self.path == "/schedule":
            self.path = "schedule_create.html"
        elif self.path == "/qa/create":
            self.path = "qa_create.html"
        elif self.path == "/demand":
            self.path = "demand_viewall"
        elif self.path == "/product":
            self.path = "product_viewall"
        elif self.path == "/rawmaterials":
            self.path = "rawmaterials_viewall"
        elif self.path == "/schedule/view":
            self.path = "schedule_view.html"
        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            elif self.path == "order_viewall":
                orders = db.select_all("orders")
                for order in orders:
                    product_name = db.get_product_name(order[1])
                    self.wfile.write(product_name)
                    self.wfile.write(order)
                    self.wfile.write("\n")
            elif self.path == "maintenance_viewall":
                self.print_query(db.select_all("maintenance"))
            elif self.path == "qa_viewall":
                self.print_query(db.select_all("qa"))
            elif self.path == "demand_viewall":
                self.print_query(db.select_all("demand"))
            elif self.path == "product_viewall":
                self.print_query(db.select_all("product"))
            elif self.path == "rawmaterials_viewall":
                self.print_query(db.select_all("rawmaterials"))
            if sendReply == True:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)


    def do_POST(self):
        if self.path=="/order/create/send":
            form = self.get_form();
            self.send_response(200)
            self.end_headers()
            product_id = int(form["product_id"].value)
            order_quantity = int(form["order_quantity"].value)
            db.raw_materials_handler(product_id, order_quantity)
            order_id = db.insert_order(product_id, form["order_quantity"].value)
            product_name = db.get_product_name(product_id)
            print "Received order for: %s" % product_name 
            self.wfile.write("Order id %d for %d %s(s)" % (order_id, int(form["order_quantity"].value), product_name))
        elif self.path == "/order/view/get":
            form = self.get_form();
            order_info = db.select_one("orders", int(form["order_id"].value))
            self.wfile.write(order_info);

        elif self.path == "/order/update/get":
            form = self.get_form()
            db.update_order(int(form["order_id"].value), form["order_status"].value, form["notes"].value)
            self.wfile.write("Order %d updated to %s" % (int(form["order_id"].value), form["order_status"].value))
            order_info = db.select_one(int(form["order_id"].value))
            self.wfile.write(order_info);

        elif self.path == "/maintenance/create/send":
            form = self.get_form() 
            maintenance_id = db.insert_maintenance(int(form["machine_id"].value), form["feedback"].value)
            self.wfile.write("Maintenance Order %d created" % maintenance_id);

        elif self.path == "/maintenance/view/get":
            form = self.get_form();
            order_info = db.select_one("maintenance", int(form["maintenance_id"].value))
            self.wfile.write(order_info);

        elif self.path == "/qa/create/send":
            form = self.get_form() 
            qa_id = db.insert_qa(int(form["product_id"].value), form["feedback"].value)
            self.wfile.write("QA Order %d created" % qa_id);

        elif self.path == "/schedule/send":
            form = self.get_form()
            schedule_id = db.create_schedule(int(form["order_id"].value), form["labour_ids"].value, form["machine_ids"].value, form["start_date"].value, form["finish_date"].value)
            self.wfile.write("Schedule %d created" % schedule_id);
            
        elif self.path == "/schedule/view/get":
            form = self.get_form();
            schedule_id = int(form["schedule_id"].value)
            schedule_info = db.select_one("schedule", schedule_id)
            self.wfile.write(schedule_info);
            self.wfile.write("\nLabour\n")
            labour_info = db.get_labour(schedule_id)
            self.wfile.write(labour_info)
            self.wfile.write("\nMachines\n")
            machine_info = db.get_machine(schedule_id)
            self.wfile.write(machine_info)

        elif self.path == "/qa/create/send":
            form = self.get_form() 
            qa_id = db.insert_qa(int(form["product_id"].value), form["feedback"].value)
            self.wfile.write("QA Order %d created" % qa_id);


        return
            
    def get_form(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {'REQUEST_METHOD':'POST',
              'CONTENT_TYPE':self.headers['Content-Type']
        })
        return form

    def print_query(self, result):
        for row in result:
            self.wfile.write(row)
            self.wfile.write("\n")
        return
            
    

try:
    db.connect_db() 
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    server.socket.close()

