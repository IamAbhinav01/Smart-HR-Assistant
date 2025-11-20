export function FileUploader({
  handleClick,
  handleDrop,
  handleFileChange,
  fileName,
  fileInputRef,
}) {
  return (
    <div
      className="border-2 border-dashed rounded-lg px-4 py-8 flex flex-col text-center items-center justify-center gap-3 cursor-pointer border-[#518EF8] hover:bg-[#f7faff] transition"
      onClick={handleClick}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <p className="text-[#313136] text-lg md:text-xl font-normal">
        Drag and Drop your resume here
      </p>
      <span className="font-normal text-sm md:text-base text-[#31313680]">
        or click browse (PDF only)
      </span>
      <input
        type="file"
        className="hidden"
        ref={fileInputRef}
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
      />
      <span>{fileName}</span>
    </div>
  );
}
