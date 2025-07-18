<html>
    <head>
        <title>Enhanced Form with Tailwind CSS</title>
        <!-- Tailwind CSS CDN -->
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .form-input:focus {
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
                transition: all 0.2s ease;
            }
            .btn-submit:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
<body class="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen flex flex-col items-center py-8">
<h1 class="text-3xl font-bold mb-6 text-blue-700">Enhanced Form with Tailwind</h1>

<?php
$name = $_POST['name'] ?? '';
if (strlen($name) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Nama: " . htmlspecialchars($name) . "</div>";
}

$email = $_POST['email'] ?? '';
if (strlen($email) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Email: " . htmlspecialchars($email) . "</div>";
}

$phone = $_POST['phone'] ?? '';
if (strlen($phone) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Telepon: " . htmlspecialchars($phone) . "</div>";
}

$password = $_POST['password'] ?? '';
if (strlen($password) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Sandi: " . htmlspecialchars($password) . "</div>";
}

$birthdate = $_POST['tanggal_lahir'] ?? '';
if (strlen($birthdate) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Tanggal Lahir: " . htmlspecialchars($birthdate) . "</div>";
}

$comment = $_POST['comment'] ?? '';
if (strlen($comment) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Komentar: " . htmlspecialchars($comment) . "</div>";
}

$gender = $_POST['gender'] ?? '';
if (strlen($gender) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Gender: " . htmlspecialchars($gender) . "</div>";
}

$hobi = $_POST['hobi'] ?? [];
if (!empty($hobi)) {
    foreach ($hobi as $h) {
        echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Hobi: " . htmlspecialchars($h) . "</div>";
    }
}

$foto = $_POST['foto'] ?? '';
if (strlen($foto) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Foto: " . htmlspecialchars($foto) . "</div>";
}

$rating = $_POST['rating'] ?? '';
if (strlen($rating) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Rating: " . htmlspecialchars($rating) . "</div>";
}

$favcolor = $_POST['favcolor'] ?? '';
if (strlen($favcolor) > 0) {
    echo "<div class='mb-2 p-2 bg-green-100 text-green-800 rounded'>Warna Favorit: " . htmlspecialchars($favcolor) . "</div>";
}
?>

<hr class="my-6 border-gray-300 w-full max-w-lg" />

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
    <div class="mb-6">
        <label for="input_nama" class="block font-semibold mb-2 text-gray-700">Name:</label>
        <input type="text" name="name" value="<?php echo htmlspecialchars($name);?>" id="input_nama" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_email" class="block font-semibold mb-2 text-gray-700">Email:</label>
        <input type="email" name="email" value="<?php echo htmlspecialchars($email);?>" id="input_email" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_phone" class="block font-semibold mb-2 text-gray-700">Telepon:</label>
        <input type="tel" name="phone" value="<?php echo htmlspecialchars($phone);?>" id="input_phone" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_password" class="block font-semibold mb-2 text-gray-700">Password:</label>
        <input type="password" name="password" value="<?php echo htmlspecialchars($password);?>" id="input_password" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="tanggal_lahir" class="block font-semibold mb-2 text-gray-700">Tanggal Lahir:</label>
        <input type="date" id="tanggal_lahir" name="tanggal_lahir" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_time" class="block font-semibold mb-2 text-gray-700">Waktu:</label>
        <input type="time" id="input_time" name="time" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_number" class="block font-semibold mb-2 text-gray-700">Jumlah:</label>
        <input type="number" id="input_number" name="number" min="1" max="100" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_range" class="block font-semibold mb-2 text-gray-700">Rating (<?php echo htmlspecialchars($rating ?? 5); ?>):</label>
        <input type="range" id="input_range" name="rating" min="1" max="10" value="<?php echo htmlspecialchars($rating ?? 5); ?>" 
               class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" />
    </div>

    <div class="mb-6">
        <label for="input_color" class="block font-semibold mb-2 text-gray-700">Warna Favorit:</label>
        <input type="color" id="input_color" name="favcolor" value="<?php echo htmlspecialchars($favcolor ?? '#ff0000'); ?>" 
               class="w-full h-10 cursor-pointer" />
    </div>

    <div class="mb-6">
        <label for="input_url" class="block font-semibold mb-2 text-gray-700">Website:</label>
        <input type="url" id="input_url" name="website" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="input_search" class="block font-semibold mb-2 text-gray-700">Pencarian:</label>
        <input type="search" id="input_search" name="search" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Komentar:</label>
        <textarea name="comment" rows="5" 
                  class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500"><?php echo htmlspecialchars($comment);?></textarea>
    </div>

    <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Gender:</label>
        <div class="flex gap-4">
            <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="female") echo "checked ";?> value="female" class="mr-2 h-4 w-4 text-blue-600">Cew</label>
            <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="male") echo "checked ";?> value="male" class="mr-2 h-4 w-4 text-blue-600">Cow</label>
            <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="other") echo "checked ";?> value="other" class="mr-2 h-4 w-4 text-blue-600">Rahasia</label>
        </div>
    </div>

    <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Hobi:</label>
        <div class="grid grid-cols-2 gap-2">
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="membaca" class="mr-2 h-4 w-4 text-blue-600">Membaca</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="nonton" class="mr-2 h-4 w-4 text-blue-600">Nonton</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="tidur" class="mr-2 h-4 w-4 text-blue-600">Tidur</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="olahraga" class="mr-2 h-4 w-4 text-blue-600">Olahraga</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="musik" class="mr-2 h-4 w-4 text-blue-600">Musik</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="game" class="mr-2 h-4 w-4 text-blue-600">Game</label>
        </div>
    </div>

    <div class="mb-6">
        <label for="foto" class="block font-semibold mb-2 text-gray-700">Foto:</label>
        <input type="file" name="foto" id="foto" 
               class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500" />
    </div>

    <div class="mb-6">
        <label for="job" class="block font-semibold mb-2 text-gray-700">Pekerjaan:</label>
        <select name="job" id="job" class="w-full border border-gray-300 rounded-lg px-4 py-2 form-input focus:border-blue-500">
            <option value="pelajar">Pelajar</option>
            <option value="mahasiswa">Mahasiswa</option>
            <option value="pns">PNS</option>
            <option value="swasta">Swasta</option>
            <option value="wiraswasta">Wiraswasta</option>
            <option value="lainnya">Lainnya</option>
        </select>
    </div>

    <div class="flex gap-4 mt-8">
        <input type="reset" name="reset" value="Reset" 
               class="px-6 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 cursor-pointer transition-all duration-200" />
        <input type="submit" name="submit" value="Submit" 
               class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer btn-submit transition-all duration-200" />
    </div>
</form>
</body>
</html>