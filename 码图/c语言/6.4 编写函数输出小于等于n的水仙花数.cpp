int find(int n) {
	int count = 0, i = 100;
	int a, b, c;
	if (n >= 1000)
		return 0;
		for (i = 100; i <= n ; i++)
		{
			a = i / 100;
			b = (i - a * 100) / 10;
			c = i % 10;
			if (i == a * a * a + b * b * b + c * c * c)
			{
				count++;
			}
		}

	return count;
}