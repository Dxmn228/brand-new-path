INSERT INTO public.bookings (user_id,session_id,seats,total_price,status,payment_status,"comment") VALUES
	 (1,1,2,3000.00,'confirmed','paid','Просим гида говорить громче'),
	 (2,1,1,1500.00,'pending','unpaid',NULL),
	 (3,3,2,7000.00,'confirmed','paid','Без острого'),
	 (4,6,1,1200.00,'completed','paid','Всё понравилось'),
	 (5,4,3,10500.00,'confirmed','paid',NULL),
	 (2,4,1,3500.00,'cancelled','refunded','Планы изменились');
