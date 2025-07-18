<html>
    <head>
        <title>Formulir Modern Tailwind</title>
        <!-- Tailwind CSS CDN -->
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                background: linear-gradient(135deg, #f0f4f8 0%, #cfe2f3 100%);
            }
            .glass {
                background: rgba(255,255,255,0.8);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(4px);
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.18);
            }
        </style>
    </head>
<body class="min-h-screen flex flex-col items-center py-8">
<h1 class="text-4xl font-extrabold mb-8 text-blue-700 drop-shadow-lg">Formulir Modern</h1>

<?php
$name = $_POST['name'] ?? '';
$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';
$birthdate = $_POST['tanggal_lahir'] ?? '';
$comment = $_POST['comment'] ?? '';
$gender = $_POST['gender'] ?? '';
$hobi = $_POST['hobi'] ?? [];
$foto = $_POST['foto'] ?? '';
$job = $_POST['job'] ?? '';
$color = $_POST['color'] ?? '';
$website = $_POST['website'] ?? '';
$range = $_POST['range'] ?? '';
$agree = $_POST['agree'] ?? '';

if (strlen($name) > 0) {
    echo "<div class='mb-2 text-green-700'>Nama: " . htmlspecialchars($name) . "</div>";
}
if (strlen($email) > 0) {
    echo "<div class='mb-2 text-green-700'>Email: " . htmlspecialchars($email) . "</div>";
}
if (strlen($password) > 0) {
    echo "<div class='mb-2 text-green-700'>Sandi: " . htmlspecialchars($password) . "</div>";
}
if (strlen($birthdate) > 0) {
    echo "<div class='mb-2 text-green-700'>Tanggal Lahir: " . htmlspecialchars($birthdate) . "</div>";
}
if (strlen($comment) > 0) {
    echo "<div class='mb-2 text-green-700'>Komentar: " . htmlspecialchars($comment) . "</div>";
}
if (strlen($gender) > 0) {
    echo "<div class='mb-2 text-green-700'>Gender: " . htmlspecialchars($gender) . "</div>";
}
if (!empty($hobi)) {
    foreach ($hobi as $h) {
        echo "<div class='mb-2 text-green-700'>Hobi: " . htmlspecialchars($h) . "</div>";
    }
}
if (strlen($foto) > 0) {
    echo "<div class='mb-2 text-green-700'>Foto: " . htmlspecialchars($foto) . "</div>";
}
if (strlen($job) > 0) {
    echo "<div class='mb-2 text-green-700'>Pekerjaan: " . htmlspecialchars($job) . "</div>";
}
if (strlen($color) > 0) {
    echo "<div class='mb-2 text-green-700'>Warna Favorit: " . htmlspecialchars($color) . "</div>";
}
if (strlen($website) > 0) {
    echo "<div class='mb-2 text-green-700'>Website: " . htmlspecialchars($website) . "</div>";
}
if (strlen($range) > 0) {
    echo "<div class='mb-2 text-green-700'>Nilai Range: " . htmlspecialchars($range) . "</div>";
}
if ($agree === 'on') {
    echo "<div class='mb-2 text-green-700'>Setuju dengan syarat dan ketentuan.</div>";
}
?>

<hr class="my-6 border-gray-300" />

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" class="glass p-10 rounded-xl shadow-xl w-full max-w-2xl border border-blue-200">
<div class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
        <label for="input_nama" class="block font-semibold mb-1 text-blue-800">Name:</label>
        <input type="text" name="name" value="<?php echo htmlspecialchars($name);?>" id="input_nama" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
    </div>
    <div>
        <label for="email" class="block font-semibold mb-1 text-blue-800">Email:</label>
        <input type="email" name="email" value="<?php echo htmlspecialchars($email);?>" id="email" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
    </div>
    <div>
        <label class="block font-semibold mb-1 text-blue-800">Password:</label>
        <input type="password" class="sandi w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" name="password" value="<?php echo htmlspecialchars($password);?>" />
    </div>
    <div>
        <label for="tanggal_lahir" class="block font-semibold mb-1 text-blue-800">Tanggal Lahir:</label>
        <input type="date" id="tanggal_lahir" name="tanggal_lahir" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
    </div>
    <div class="col-span-2">
        <label class="block font-semibold mb-1 text-blue-800">Komentar:</label>
        <textarea name="comment" rows="3" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400"><?php echo htmlspecialchars($comment);?></textarea>
    </div>
    <div>
        <label class="block font-semibold mb-1 text-blue-800">Gender:</label>
        <div class="flex gap-4">
            <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="female") echo "checked ";?> value="female" class="mr-2">Cew</label>
            <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="male") echo "checked ";?> value="male" class="mr-2">Cow</label>
            <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="other") echo "checked ";?> value="other" class="mr-2">Rahasia</label>
        </div>
    </div>
    <div>
        <label class="block font-semibold mb-1 text-blue-800">Hobi:</label>
        <div class="flex gap-4 flex-wrap">
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="membaca" class="mr-2">Membaca</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="nonton" class="mr-2">Nonton</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="tidur" class="mr-2">Tidur</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="olahraga" class="mr-2">Olahraga</label>
            <label class="flex items-center"><input type="checkbox" name="hobi[]" value="musik" class="mr-2">Musik</label>
        </div>
    </div>
    <div>
        <label for="foto" class="block font-semibold mb-1 text-blue-800">Foto:</label>
        <input type="file" name="foto" id="foto" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
    </div>
    <div>
        <label for="job" class="block font-semibold mb-1 text-blue-800">Pekerjaan:</label>
        <select name="job" id="job" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400">
            <option value="pelajar">Pelajar</option>
            <option value="mahasiswa">Mahasiswa</option>
            <option value="pns">PNS</option>
            <option value="swasta">Swasta</option>
            <option value="wiraswasta">Wiraswasta</option>
            <option value="lainnya">Lainnya</option>
        </select>
    </div>
    <div>
        <label for="color" class="block font-semibold mb-1 text-blue-800">Warna Favorit:</label>
        <input type="color" name="color" id="color" value="<?php echo htmlspecialchars($color);?>" class="w-16 h-10 border border-blue-300 rounded" />
    </div>
    <div>
        <label for="website" class="block font-semibold mb-1 text-blue-800">Website:</label>
        <input type="url" name="website" id="website" value="<?php echo htmlspecialchars($website);?>" class="w-full border border-blue-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
    </div>
    <div>
        <label for="range" class="block font-semibold mb-1 text-blue-800">Nilai Range:</label>
        <input type="range" name="range" id="range" min="0" max="100" value="<?php echo htmlspecialchars($range);?>" class="w-full" />
    </div>
    <div class="col-span-2 flex items-center mt-2">
        <input type="checkbox" name="agree" id="agree" class="mr-2">
        <label for="agree" class="text-blue-800">Saya setuju dengan syarat dan ketentuan</label>
    </div>
</div>
<div class="flex gap-4 mt-8 justify-center">
    <input type="reset" name="reset" value="Reset" class="px-6 py-2 bg-gray-200 rounded hover:bg-gray-300 cursor-pointer font-semibold shadow" />
    <input type="submit" name="submit" value="Submit" class="px-6 py-2 bg-gradient-to-r from-blue-600 to-blue-400 text-white rounded hover:from-blue-700 hover:to-blue-500 cursor-pointer font-semibold shadow-lg" />
</div>
</form>
</body>
</html>
