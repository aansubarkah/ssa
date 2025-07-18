<html>
    <head>
        <title>Formulir Tailwind V2</title>
        <!-- Tailwind CSS CDN -->
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            /* Custom styles for a more compelling look */
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-radius: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.3);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            /* Custom focus style for better accessibility */
            input:focus, textarea:focus, select:focus {
                --tw-ring-color: #a78bfa;
            }
        </style>
    </head>
<body class="min-h-screen flex flex-col items-center justify-center p-4 text-gray-800">

<?php
// --- PHP Data Handling ---

// Use null coalescing operator for cleaner variable assignments
$name = $_POST['name'] ?? '';
$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';
$birthdate = $_POST['tanggal_lahir'] ?? '';
$comment = $_POST['comment'] ?? '';
$gender = $_POST['gender'] ?? '';
$hobi = $_POST['hobi'] ?? [];
$foto = $_FILES['foto']['name'] ?? ''; // For file uploads, it's better to check $_FILES
$job = $_POST['job'] ?? '';
$website = $_POST['website'] ?? '';
$color = $_POST['color'] ?? '#ffffff';
$satisfaction = $_POST['satisfaction'] ?? '50';
$agree = isset($_POST['agree']);

$is_submitted = !empty($_POST);

if ($is_submitted) {
    echo "<div class='glass-card p-6 w-full max-w-2xl mb-8 text-white'>";
    echo "<h2 class='text-2xl font-bold mb-4 border-b border-gray-400 pb-2'>Data yang Dikirim:</h2>";

    if (strlen($name) > 0) echo "<p><strong>Nama:</strong> " . htmlspecialchars($name) . "</p>";
    if (strlen($email) > 0) echo "<p><strong>Email:</strong> " . htmlspecialchars($email) . "</p>";
    // It's a bad practice to display password, but doing so for demonstration
    if (strlen($password) > 0) echo "<p><strong>Sandi:</strong> " . htmlspecialchars($password) . "</p>";
    if (strlen($birthdate) > 0) echo "<p><strong>Tanggal Lahir:</strong> " . htmlspecialchars($birthdate) . "</p>";
    if (strlen($comment) > 0) echo "<p><strong>Komentar:</strong> " . htmlspecialchars($comment) . "</p>";
    if (strlen($gender) > 0) echo "<p><strong>Gender:</strong> " . htmlspecialchars($gender) . "</p>";
    if (strlen($job) > 0) echo "<p><strong>Pekerjaan:</strong> " . htmlspecialchars($job) . "</p>";
    if (strlen($website) > 0) echo "<p><strong>Website:</strong> " . htmlspecialchars($website) . "</p>";
    if (strlen($color) > 0) echo "<p><strong>Warna Favorit:</strong> <span style='background-color:" . htmlspecialchars($color) ."; padding: 2px 10px; border-radius: 4px; border: 1px solid #fff;'>" . htmlspecialchars($color) . "</span></p>";
    if (strlen($satisfaction) > 0) echo "<p><strong>Tingkat Kepuasan:</strong> " . htmlspecialchars($satisfaction) . "</p>";
    if (strlen($foto) > 0) echo "<p><strong>Nama File Foto:</strong> " . htmlspecialchars($foto) . "</p>";

    if (!empty($hobi)) {
        echo "<p><strong>Hobi:</strong> " . htmlspecialchars(implode(', ', $hobi)) . "</p>";
    }
    
    echo "<p><strong>Setuju S&K:</strong> " . ($agree ? 'Ya' : 'Tidak') . "</p>";
    
    echo "</div>";
}

?>

<div class="glass-card p-8 w-full max-w-4xl">
    <h1 class="text-4xl font-extrabold mb-6 text-center text-white drop-shadow-lg">Formulir Pendaftaran V2</h1>

    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" enctype="multipart/form-data">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Name -->
            <div>
                <label for="input_nama" class="block font-semibold mb-1 text-white">Nama Lengkap:</label>
                <input type="text" name="name" value="<?php echo htmlspecialchars($name);?>" id="input_nama" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none" required />
            </div>

            <!-- Email -->
            <div>
                <label for="email" class="block font-semibold mb-1 text-white">Email:</label>
                <input type="email" name="email" value="<?php echo htmlspecialchars($email);?>" id="email" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none" required />
            </div>

            <!-- Password -->
            <div>
                <label for="password" class="block font-semibold mb-1 text-white">Password:</label>
                <input type="password" id="password" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none" name="password" value="<?php echo htmlspecialchars($password);?>" required />
            </div>

            <!-- Birth Date -->
            <div>
                <label for="tanggal_lahir" class="block font-semibold mb-1 text-white">Tanggal Lahir:</label>
                <input type="date" id="tanggal_lahir" name="tanggal_lahir" value="<?php echo htmlspecialchars($birthdate); ?>" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none" />
            </div>

            <!-- Gender -->
            <div class="md:col-span-2">
                <label class="block font-semibold mb-1 text-white">Gender:</label>
                <div class="flex gap-4 mt-2 text-white">
                    <label class="flex items-center"><input type="radio" name="gender" <?php if ($gender=="female") echo "checked";?> value="female" class="mr-2 h-4 w-4">Wanita</label>
                    <label class="flex items-center"><input type="radio" name="gender" <?php if ($gender=="male") echo "checked";?> value="male" class="mr-2 h-4 w-4">Pria</label>
                    <label class="flex items-center"><input type="radio" name="gender" <?php if ($gender=="other") echo "checked";?> value="other" class="mr-2 h-4 w-4">Lainnya</label>
                </div>
            </div>

            <!-- Hobbies -->
            <div class="md:col-span-2">
                <label class="block font-semibold mb-1 text-white">Hobi:</label>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2 text-white">
                    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="membaca" <?php if (in_array('membaca', $hobi)) echo 'checked'; ?> class="mr-2 h-4 w-4 rounded">Membaca</label>
                    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="nonton" <?php if (in_array('nonton', $hobi)) echo 'checked'; ?> class="mr-2 h-4 w-4 rounded">Nonton</label>
                    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="tidur" <?php if (in_array('tidur', $hobi)) echo 'checked'; ?> class="mr-2 h-4 w-4 rounded">Tidur</label>
                    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="gaming" <?php if (in_array('gaming', $hobi)) echo 'checked'; ?> class="mr-2 h-4 w-4 rounded">Gaming</label>
                    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="olahraga" <?php if (in_array('olahraga', $hobi)) echo 'checked'; ?> class="mr-2 h-4 w-4 rounded">Olahraga</label>
                    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="koding" <?php if (in_array('koding', $hobi)) echo 'checked'; ?> class="mr-2 h-4 w-4 rounded">Koding</label>
                </div>
            </div>

            <!-- Job -->
            <div>
                <label for="job" class="block font-semibold mb-1 text-white">Pekerjaan:</label>
                <select name="job" id="job" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none">
                    <option value="pelajar" <?php if ($job == 'pelajar') echo 'selected'; ?>>Pelajar</option>
                    <option value="mahasiswa" <?php if ($job == 'mahasiswa') echo 'selected'; ?>>Mahasiswa</option>
                    <option value="pns" <?php if ($job == 'pns') echo 'selected'; ?>>PNS</option>
                    <option value="swasta" <?php if ($job == 'swasta') echo 'selected'; ?>>Swasta</option>
                    <option value="wiraswasta" <?php if ($job == 'wiraswasta') echo 'selected'; ?>>Wiraswasta</option>
                    <option value="lainnya" <?php if ($job == 'lainnya') echo 'selected'; ?>>Lainnya</option>
                </select>
            </div>

            <!-- File Upload -->
            <div>
                <label for="foto" class="block font-semibold mb-1 text-white">Foto Profil:</label>
                <input type="file" name="foto" id="foto" class="w-full text-white file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100" />
            </div>

            <!-- Website -->
            <div>
                <label for="website" class="block font-semibold mb-1 text-white">Website:</label>
                <input type="url" name="website" id="website" value="<?php echo htmlspecialchars($website);?>" placeholder="https://example.com" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none" />
            </div>

            <!-- Favorite Color -->
            <div>
                <label for="color" class="block font-semibold mb-1 text-white">Warna Favorit:</label>
                <input type="color" name="color" id="color" value="<?php echo htmlspecialchars($color);?>" class="w-full h-10 p-1 bg-white/50 border border-gray-300 rounded cursor-pointer" />
            </div>

            <!-- Satisfaction Range -->
            <div class="md:col-span-2">
                <label for="satisfaction" class="block font-semibold mb-1 text-white">Tingkat Kepuasan (<?php echo htmlspecialchars($satisfaction); ?>):</label>
                <input type="range" name="satisfaction" id="satisfaction" min="0" max="100" value="<?php echo htmlspecialchars($satisfaction);?>" class="w-full h-2 bg-gray-200/50 rounded-lg appearance-none cursor-pointer" oninput="this.previousElementSibling.innerText = `Tingkat Kepuasan (${this.value}):`" />
            </div>
            
            <!-- Comment -->
            <div class="md:col-span-2">
                <label for="comment" class="block font-semibold mb-1 text-white">Komentar:</label>
                <textarea name="comment" id="comment" rows="4" class="w-full bg-white/50 border border-gray-300 rounded px-3 py-2 text-gray-800 focus:ring-2 focus:outline-none"><?php echo htmlspecialchars($comment);?></textarea>
            </div>

            <!-- Agreement -->
            <div class="md:col-span-2 flex items-center">
                <input type="checkbox" name="agree" id="agree" <?php if ($agree) echo 'checked'; ?> class="h-4 w-4 rounded mr-2" required>
                <label for="agree" class="text-white">Saya setuju dengan <a href="#" class="underline font-bold">Syarat dan Ketentuan</a></label>
            </div>

        </div>

        <!-- Buttons -->
        <div class="flex gap-4 mt-8 justify-end">
            <input type="reset" value="Reset" class="px-6 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 cursor-pointer font-semibold shadow-md transition-colors" />
            <input type="submit" value="Submit" class="px-6 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-lg hover:from-purple-600 hover:to-indigo-700 cursor-pointer font-semibold shadow-lg transition-transform transform hover:scale-105" />
        </div>
    </form>
</div>

</body>
</html>